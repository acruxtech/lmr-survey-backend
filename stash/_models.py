import datetime


class Answer:
    questoin_id: int
    text: str


class Question:
    id: int
    title: str = None               # optional. тогда вопросы по порядку пронумеруются "Вопрос №1"
    text: str
    type: str                       # may be "field" | "checkbox" | "list" | "radio"
    answers: str | list[str] = None     # список вариантов. 
    correct_answers: str | list[str]

    coefficient: int = None         # default 1
    reward: int = None              # сколько дается за правильный ответ. default 1
    sanction: int = None            # сколько отбирается за НЕправильный ответ. default 0


class Survey:
    uuid: str
    access_hash: str

    title: str
    topic: str
    is_public: bool
    show_result_after_passing: bool
    after_passing_text: str = None              # текст который покажется пользователю после прохождения
    questions: list[Question]
    passing_score: int = None                   # проходной балл
    time_to_pass: datetime.datetime = None      # in minutes


# если успеем
class User:
    name: str
    email: str
    password_hash: str              # если делать, то по крутому, с хешированием
    passed_surveys: str             # типо пройденные опросы. подумаю потом как нормализовать можно будет
