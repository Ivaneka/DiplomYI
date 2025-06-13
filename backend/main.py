import os
import secrets
import hashlib
import uuid

import fastapi
import sqlalchemy
from fastapi import HTTPException, Response, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel

from orm import Base
import orm

app = fastapi.FastAPI()


def get_database_url():
    user_file = os.getenv('POSTGRES_USER_FILE')
    password_file = os.getenv('POSTGRES_PASSWORD_FILE')
    with open(user_file) as file:
        user = file.read().strip()
    with open(password_file) as file:
        password = file.read().strip()
    url = f'postgresql://{user}:{password}@postgres:5432/tests'
    return url


db_url = get_database_url()
engine = create_engine(db_url)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


@app.get('/api/health')
def health():
    return None


class CredentialsModel(BaseModel):
    username: str
    password: str


def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


@app.post('/api/signup')
def signup(credentials: CredentialsModel):
    with Session() as session:
        existing_user = session.query(
            orm.User).filter_by(username=credentials.username).first()
    if existing_user is not None:
        raise HTTPException(400, "User already exists")
    salt = secrets.token_bytes(16)
    password_hash = hash_password(credentials.password, salt)
    new_user = orm.User(
        username=credentials.username,
        salt=salt,
        password_hash=password_hash,
    )
    with Session() as session:
        session.add(new_user)
        session.commit()
    return None


@app.post('/api/login')
def login(credentials: CredentialsModel, response: Response):
    with Session() as session:
        user: orm.User | None = session.query(
            orm.User).filter_by(username=credentials.username).first()
    if user is None:
        raise HTTPException(401, "No such user exists")
    password_hash = hash_password(credentials.password, user.salt)
    if password_hash != user.password_hash:
        raise HTTPException(401, 'Wrong password')
    cookie_token = uuid.uuid4()
    cookie = orm.Cookie(
        token=cookie_token,
        user_id=user.id,
    )
    with Session() as session:
        session.add(cookie)
        session.commit()
    response.set_cookie('session', cookie_token)
    return None


@app.middleware('http')
async def auth_middleware(request: Request, call_next):
    request.state.user = None
    session_token = request.cookies.get('session')
    if session_token is None:
        return await call_next(request)
    with Session() as session:
        cookie: orm.Cookie = session.query(
            orm.Cookie).filter_by(token=session_token).first()
        if cookie is None or cookie.is_expired():
            return await call_next(request)
        request.state.user = cookie.user
    return await call_next(request)


@app.get('/api/current_user')
def current_user(request: Request):
    return {'username': request.state.user.username}


class AnswerModel(BaseModel):
    text: str
    is_correct: bool


class QuestionModel(BaseModel):
    text: str
    options: list[AnswerModel]


class TestModel(BaseModel):
    title: str
    description: str
    material_ids: list[int]
    questions: list[QuestionModel]


class MaterialModel(BaseModel):
    title: str
    content: str


class MaterialModelWithID(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


@app.put('/api/material')
def create_material(request: Request, material: MaterialModel):
    if request.state.user is None:
        raise HTTPException(401)
    if not request.state.user.is_admin:
        raise HTTPException(403)
    orm_material = orm.Material(
        title=material.title,
        content=material.title,
    )
    with Session() as session:
        session.add(orm_material)
        session.commit()


@app.get('/api/material')
def get_materials(request: Request) -> list[MaterialModelWithID]:
    with Session() as session:
        return session.query(orm.Material).all()


@app.put('/api/test')
def create_test(request: Request, test: TestModel):
    if request.state.user is None:
        raise HTTPException(401)
    if not request.state.user.is_admin:
        raise HTTPException(403)
    orm_test = orm.Test(title=test.title,
                        description=test.description,
                        questions=[
                            orm.Question(text=question.text,
                                         answers=[
                                             orm.Answer(
                                                 text=answer.text,
                                                 is_correct=answer.is_correct,
                                             ) for answer in question.options
                                         ]) for question in test.questions
                        ])
    with Session() as session:
        session.add(orm_test)
        session.commit()
        session.refresh(orm_test)
        for material_id in test.material_ids:
            session.execute(sqlalchemy.insert(orm.test_material_links), {
                'test_id': orm_test.id,
                'material_id': material_id,
            })
        session.commit()
