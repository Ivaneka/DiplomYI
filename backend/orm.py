from datetime import datetime
from sqlalchemy import (Column, Integer, String, Text, Boolean, DateTime,
                        ForeignKey, Table, LargeBinary)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

test_material_links = Table(
    'test_material_links', Base.metadata,
    Column('test_id',
           Integer,
           ForeignKey('tests.id', ondelete='CASCADE'),
           primary_key=True),
    Column('material_id',
           Integer,
           ForeignKey('materials.id', ondelete='CASCADE'),
           primary_key=True))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    password_hash = Column(LargeBinary, nullable=False)
    is_admin = Column(Boolean, default=False)

    attempts = relationship("TestAttempt", back_populates="user")
    assigned_tests = relationship("UserAssignedTest", back_populates="user")
    cookies = relationship("Cookie",
                           back_populates="user",
                           cascade="all, delete-orphan")


class Cookie(Base):
    __tablename__ = 'cookies'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False)
    user_id = Column(Integer,
                     ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True, default=None)

    user = relationship("User", back_populates="cookies")

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return self.expires_at < datetime.utcnow()


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    tests = relationship("Test",
                         secondary=test_material_links,
                         back_populates="materials")


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    materials = relationship("Material",
                             secondary=test_material_links,
                             back_populates="tests")
    questions = relationship("Question",
                             back_populates="test",
                             cascade="all, delete-orphan")
    attempts = relationship("TestAttempt", back_populates="test")
    assigned_users = relationship("UserAssignedTest", back_populates="test")


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey('tests.id', ondelete='CASCADE'))
    text = Column(Text, nullable=False)

    test = relationship("Test", back_populates="questions")
    answers = relationship("Answer",
                           back_populates="question",
                           cascade="all, delete-orphan")
    attempt_answers = relationship("AttemptAnswer", back_populates="question")


class Answer(Base):
    __tablename__ = 'answers'

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id',
                                             ondelete='CASCADE'))
    text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="answers")
    attempt_answers = relationship("AttemptAnswer", back_populates="answer")


class TestAttempt(Base):
    __tablename__ = 'test_attempts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    test_id = Column(Integer, ForeignKey('tests.id', ondelete='CASCADE'))
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    score = Column(Integer)

    user = relationship("User", back_populates="attempts")
    test = relationship("Test", back_populates="attempts")
    attempt_answers = relationship("AttemptAnswer", back_populates="attempt")


class AttemptAnswer(Base):
    __tablename__ = 'attempt_answers'

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer,
                        ForeignKey('test_attempts.id', ondelete='CASCADE'))
    question_id = Column(Integer, ForeignKey('questions.id',
                                             ondelete='CASCADE'))
    answer_id = Column(Integer, ForeignKey('answers.id', ondelete='CASCADE'))

    attempt = relationship("TestAttempt", back_populates="attempt_answers")
    question = relationship("Question", back_populates="attempt_answers")
    answer = relationship("Answer", back_populates="attempt_answers")


class UserAssignedTest(Base):
    __tablename__ = 'user_assigned_tests'

    user_id = Column(Integer,
                     ForeignKey('users.id', ondelete='CASCADE'),
                     primary_key=True)
    test_id = Column(Integer,
                     ForeignKey('tests.id', ondelete='CASCADE'),
                     primary_key=True)
    assigned_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="assigned_tests")
    test = relationship("Test", back_populates="assigned_users")
