import os
import asyncio
import logging

from sqlalchemy.orm import sessionmaker

import src.endpoints.basic 
from src.utils.variables import app
from src.utils.ConnManager import ConnManager
from db.pool_creater import create_db_pool
from config import load_config


logger = logging.getLogger(__name__)


async def main():
    if(os.path.isfile('all.log')):
        os.remove('all.log')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        encoding="UTF-8",
        handlers=[
            logging.FileHandler("all.log"),
            logging.StreamHandler()
        ]
    )
    logger.error("Starting server")
    config = load_config("config.ini")

    db_pool: sessionmaker = await create_db_pool(
        user=config.db.user,
        password=config.db.password,
        address=config.db.address,
        name=config.db.name,
        echo=False,
    )

    ConnManager.set_pool(db_pool)
    app.run(debug=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

