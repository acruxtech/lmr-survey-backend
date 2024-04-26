import logging

from uuid import uuid4
from typing import Iterable
from datetime import date, time
from sqlalchemy import select, delete, and_, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Survey, Question, Answer


logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""


    def __init__(self, conn):
        self.conn: AsyncSession = conn


    async def add_survey(
            self, 
            title: str,
            topic: str,
            is_public: bool, 
            show_result_after_passing: bool,
            questions: list[dict],
            after_passing_text: str = None,
            passing_score: str = None,
            time_to_pass: str = None,
        ) -> Survey:

        survey = Survey(
            uuid=str(uuid4()),
            access_hash=str(uuid4()),
            title=title,
            topic=topic,
            is_public=is_public,
            show_result_after_passing=show_result_after_passing,
            after_passing_text=after_passing_text,
            passing_score=passing_score,
            time_to_pass=time_to_pass,
        )

        for i, question_data in enumerate(questions):
            survey.questions.append(
                Question(
                    title=question_data.get("title", f"Вопрос №{i + 1}"),
                    text=question_data["text"],
                    type=question_data["type"],
                    answers="|".join(question_data.get("answers", [])),
                    correct_answers="|".join(question_data.get("correct_answers", [])),
                    reward=question_data.get("reward", None),
                    sanction=question_data.get("sanction"),
                )
            )

        self.conn.add(survey)
        await self.conn.commit()

        return survey


    async def get_surveys(self) -> list[Survey]:
        res = await self.conn.execute(
                select(Survey).options(selectinload(Survey.answers))
            )

        return res.scalars().all()
    

    # async def get_amount_users(self) -> int:
    #     res = await self.conn.execute(
    #         "SELECT COUNT(*) from users"
    #     )
        
    #     return res.scalars().one()
    

    # async def update_user(self, telegram_id: int = None, id: int = None, jobs: list[str] = None, **kwargs):
    #     if telegram_id:
    #         user = await self.get_user_by_telegram_id(telegram_id)
    #     elif id:
    #         user = await self.get_user_by_id(id)
    #     else:
    #         raise ValueError(f'Telegram ID or id is required')

    #     if not user:
    #         raise ValueError(f'User with id {telegram_id if telegram_id else id} doesn\'t exist')
        
    #     if jobs:
    #         jobs = [await self.get_job_by_title(job_title) for job_title in jobs]
    #         user.jobs.clear()
    #         user.jobs.extend(jobs)

    #     for key, value in kwargs.items():
    #         if not hasattr(User, key):
    #             raise ValueError(f'Class `User` doesn\'t have argument {key}') 
    #         setattr(user, key, value)
    #     await self.conn.commit()


    # async def get_users_where(self, **kwargs) -> list[User] | None:
    #     res = await self.conn.execute(
    #         select(User).where(
    #             and_(
    #                 *[User.__table__.columns[k] == v for k, v in kwargs.items()]
    #             )
    #         )
    #     )
        
    #     return res.scalars().all()


    # async def delete_user(self, telegram_id: int):
    #     user = await self.get_user_by_telegram_id(telegram_id)

    #     if user is None:
    #         raise ValueError(f"User with {telegram_id=} doensn't exist") 
        
    #     await self.conn.delete(user)
    #     await self.conn.commit()
        