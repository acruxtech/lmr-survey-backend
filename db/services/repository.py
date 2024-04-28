import logging

from uuid import uuid4
from typing import Iterable
from datetime import date, time
from sqlalchemy import select, delete, and_, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.models import Survey, Question, UserResult


logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""


    def __init__(self, conn):
        self.conn: AsyncSession = conn


    async def add_survey(
            self, 
            title: str,
            topic: str,
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
            show_result_after_passing=show_result_after_passing,
            after_passing_text=after_passing_text,
            passing_score=passing_score,
            time_to_pass=time_to_pass,
        )

        for i, question_data in enumerate(questions):
            question = await self.add_question(
                title=question_data.get("title", f"Вопрос №{i + 1}"),
                text=question_data["text"],
                answers=question_data.get("answers", []),
                correct_answer=question_data["correct_answer"],
                reward=question_data.get("reward", 1),
                sanction=question_data.get("sanction", 0),
            )
            survey.questions.append(question)

        self.conn.add(survey)
        await self.conn.commit()

        return survey


    async def get_surveys(self) -> list[Survey]:
        res = await self.conn.execute(
                select(Survey).options(selectinload(Survey.questions))
            )

        return res.scalars().all()
    

    async def get_survey_by_uuid(self, uuid: str) -> Survey:
        res = await self.conn.execute(
                select(Survey).options(selectinload(Survey.questions)).where(Survey.uuid == uuid)
            )

        return res.scalars().first()
       

    async def delete_survey(self, uuid: str, access_hash: str):
        survey = await self.get_survey_by_uuid(uuid)

        if survey is None:
            return
        
        if access_hash != survey.access_hash:
            return
        
        await self.conn.delete(survey)
        await self.conn.commit()


    async def add_question(
            self, 
            text: str,
            answers: list[str],
            correct_answer: str,
            title: str = None,
            reward: int = 1,
            sanction: int = 0,
        ) -> Question:

        question = Question(
            title=title,
            text=text,
            answers="|".join(answers),
            correct_answer=correct_answer,
            reward=reward,
            sanction=sanction,
        )

        self.conn.add(question)
        await self.conn.commit()

        return question
    

    async def add_user_result(
            self, 
            answers: list[str],
            score: int,
            survey: Survey
        ) -> UserResult:

        user_result = UserResult(
            text="|".join(answers),
            score=score,
        )

        self.conn.add(user_result)
        survey.user_results.append(user_result)
        await self.conn.commit()

        return user_result
