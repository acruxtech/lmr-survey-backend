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

            res = await func(**kwargs)

            del kwargs["repo"]
            db = kwargs.get("db")
            if db:
                await db.close()

            return res

        wrapper.__name__ = func.__name__
        return wrapper