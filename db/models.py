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
    is_public = Column(Boolean)
    show_result_after_passing = Column(Boolean)
    after_passing_text = Column(Text, nullable=True)            # текст, который покажется пользователю после прохождения
    passing_score = Column(Integer, nullable=True)              # проходной балл
    time_to_pass = Column(Integer, nullable=True)               # в минутах

    questions = relationship("Question")
    answers = relationship("Answer")


class Question(BaseCommon):
    __tablename__ = "questions"

    title = Column(Text, nullable=True)                         # optional. тогда вопросы по порядку пронумеруются "Вопрос №1"
    text = Column(Text)
    type = Column(Text)                                         # may be "field" | "checkbox" | "list" | "radio"
    answers = Column(Text, nullable=True)                       # список вариантов через |
    correct_answers = Column(Text, nullable=True)               # список правильных ответов через |

    reward = Column(Integer, default=1)                         # сколько дается за правильный ответ
    sanction = Column(Integer, default=0)                       # сколько отбирается за неправильный ответ

    survey = relationship("Survey", back_populates="questions")


class Answer:
    __tablename__ = "answers"
    
    text = Column(Text, nullable=True)                          # список правильных ответов через |

    survey = relationship("Survey", back_populates="answers")
