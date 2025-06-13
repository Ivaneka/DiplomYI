import os
import secrets
import hashlib
import uuid

import fastapi
import sqlalchemy
from fastapi import HTTPException, Response, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from pydantic import BaseModel

from orm import Base
import orm

app = fastapi.FastAPI()


def get_database_url():
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
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
        content=material.content,
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


class ORMAnswer(BaseModel):
    id: int
    is_correct: bool
    text: str

    class Config:
        orm_mode = True


class ORMQuestion(BaseModel):
    text: str
    answers: list[ORMAnswer]

    class Config:
        orm_mode = True


class ORMTest(BaseModel):
    id: int
    title: str
    description: str
    questions: list[ORMQuestion]

    class Config:
        orm_mode = True


class ORMUser(BaseModel):
    username: str
    assigned_tests: list[ORMTest]

    class Config:
        orm_mode = True


@app.get('/api/tests/assigned')
def get_tests(request: Request, username: str) -> list[ORMTest]:
    if request.state.user is None:
        raise HTTPException(401)
    if not request.state.user.is_admin and request.state.user.username != username:
        raise HTTPException(403)
    with Session() as session:
        return session.query(orm.Test).join(
            orm.UserAssignedTest,
            orm.UserAssignedTest.test_id == orm.Test.id).join(
                orm.User,
                orm.UserAssignedTest.user_id == orm.User.id).filter_by(
                    username=username).options(
                        joinedload(orm.Test.questions).subqueryload(
                            orm.Question.answers)).all()


class ORMAttemptAnswer(BaseModel):
    answer: ORMAnswer


class ORMAttempt(BaseModel):
    attempt_answers: list[ORMAttemptAnswer]


@app.get('/api/attempt')
def get_attempts(request: Request, username: str,
                 test_id: int) -> list[ORMAttempt]:
    if request.state.user is None:
        raise HTTPException(401)
    if not request.state.user.is_admin and request.state.user.username != username:
        raise HTTPException(403)
    with Session() as session:
        return session.query(orm.TestAttempt).filter_by(test_id=test_id).join(
            orm.User, orm.TestAttempt.user_id == orm.User.id).options(
                joinedload(orm.TestAttempt.attempt_answers).subqueryload(
                    orm.AttemptAnswer.answer)).filter_by(
                        username=username).all()


@app.get('/api/me')
def get_me(request: Request):
    if request.state.user is None:
        return {'username': None}
    return {'username': request.state.user.username}


class AttemptRequest(BaseModel):
    selectedAnswers: list[int]
    test_id: int


@app.put('/api/attempt')
def add_attempt(request: Request, attempt_: AttemptRequest):
    if request.state.user is None:
        raise HTTPException(401)
    with Session() as session:
        attempt = orm.TestAttempt(user_id=request.state.user.id,
                                  test_id=attempt_.test_id)
        session.add(attempt)
        session.commit()
        session.refresh(attempt)
        for answer_id in attempt_.selectedAnswers:
            attempt_answer = orm.AttemptAnswer(attempt_id=attempt.id,
                                               answer_id=answer_id)
            session.add(attempt_answer)
            session.commit()
            session.refresh(attempt_answer)
            if attempt_answer.answer.is_correct:
                attempt.score += 1
                session.commit()


@app.get('/api/user')
def get_users(request: Request):
    if request.state.user is None:
        raise HTTPException(401)
    if not request.state.user.is_admin:
        raise HTTPException(403)
    with Session() as session:
        res = session.query(orm.User.username).all()
        return [username for username, in res]


class AssignRequest(BaseModel):
    username: str
    test_id: int


@app.post('/api/assign')
def assign_test(request: Request, body: AssignRequest):
    if request.state.user is None:
        raise HTTPException(401)
    if not request.state.user.is_admin:
        raise HTTPException(403)
    with Session() as session:
        user = session.query(
            orm.User).filter_by(username=body.username).first()
        if user is None:
            raise HTTPException(400)
        assignment = orm.UserAssignedTest(user_id=user.id,
                                          test_id=body.test_id)
        session.add(assignment)
        session.commit()


@app.get('/api/test')
def get_all_tests(request: Request):
    if request.state.user is None:
        raise HTTPException(401)
    if not request.state.user.is_admin:
        raise HTTPException(403)
    with Session() as session:
        return session.query(orm.Test).all()


with Session() as session:
    existing_user = session.query(orm.User).filter_by(username='admin').first()
if existing_user is None:
    salt = secrets.token_bytes(16)
    password_hash = hash_password('admin', salt)
    new_user = orm.User(
        username='admin',
        salt=salt,
        password_hash=password_hash,
        is_admin=True,
    )
    with Session() as session:
        session.add(new_user)
        session.commit()
