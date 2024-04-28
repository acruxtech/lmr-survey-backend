from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
 
from db.base import Base


class BaseCommon(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Survey(BaseCommon):
    __tablename__ = "surveys"

    uuid = Column(Text)
    access_hash = Column(Text)

    title = Column(Text)
    topic = Column(Text)
    show_result_after_passing = Column(Boolean)
    after_passing_text = Column(Text, nullable=True)            # текст, который покажется пользователю после прохождения
    passing_score = Column(Integer, nullable=True)              # проходной балл
    time_to_pass = Column(Integer, nullable=True)               # в минутах

    questions = relationship("Question", lazy="selectin")
    user_results = relationship("UserResult", lazy="selectin")


class Question(BaseCommon):
    __tablename__ = "questions"

    title = Column(Text, nullable=True)                         # optional. тогда вопросы по порядку пронумеруются "Вопрос №1"
    text = Column(Text)
    answers = Column(Text)                                      # список вариантов через |
    correct_answer = Column(Text)                               # правильный ответ

    reward = Column(Integer, default=1)                         # сколько дается за правильный ответ
    sanction = Column(Integer, default=0)                       # сколько отбирается за неправильный ответ

    survey_id = Column(Integer, ForeignKey("surveys.id"))
    survey = relationship("Survey", back_populates="questions")


class UserResult(BaseCommon):
    __tablename__ = "user_results"
    
    text = Column(Text)                                         # список ответов через |
    score = Column(Integer)                                     # сколько баллов получил/потерял человек
    
    survey_id = Column(Integer, ForeignKey("surveys.id"))
    survey = relationship("Survey", back_populates="user_results")
