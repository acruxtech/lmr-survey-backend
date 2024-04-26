from sqlalchemy.ext.asyncio import AsyncSession
from db.services.repository import Repo


class ConnManager:
    pool = None

    @staticmethod
    def set_pool(pool):
        ConnManager.pool = pool


    @staticmethod
    def db_decorator(func):

        async def wrapper():
            db: AsyncSession = ConnManager.pool()

            kwargs = {}
            kwargs["db"] = db
            kwargs["repo"] = Repo(db)

            return await func(**kwargs)

        return wrapper