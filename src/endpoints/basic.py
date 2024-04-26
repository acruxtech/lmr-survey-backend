from src.utils.variables import app
from src.utils.ConnManager import ConnManager
from db.services.repository import Repo


@app.route("/")
@ConnManager.db_decorator
async def hello_world(repo: Repo, **kwargs):
    print(kwargs)
    await repo.add_user()
    return "<p>Hello, World!</p>"

