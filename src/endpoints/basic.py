import logging
from flask import request

from src.utils.functions import get_survey_json
from src.utils.variables import app
from src.utils.ConnManager import ConnManager
from db.services.repository import Repo


logger = logging.getLogger(__name__)


@ConnManager.db_decorator
async def create(repo: Repo, **kwargs):
    data = request.get_json(force=True)

    try:
        survey = await repo.add_survey(
            title=data["title"],
            topic=data["topic"],
            show_result_after_passing=data["show_result_after_passing"],
            questions=data["questions"],
            after_passing_text=data.get("after_passing_text", None),
            passing_score=data.get("passing_score", None),
            time_to_pass=data.get("time_to_pass", None),
        )
    except BaseException as e:
        logger.error(e)
        return "Bad format! Be careful", 400
    
    return {
        "uuid": survey.uuid,
        "access_hash": survey.access_hash
    }


@ConnManager.db_decorator
async def surveys(repo: Repo, **kwargs):
    """Возвращает опросы. Все - если фильтры не переданы.
    Возможные фильтры:
        1. sorted_by (str, may be "new", "short", "popular")
        2. from (int, порядковый номер опроса, с которого надо начинать)
        2. to (int, порядковый номер опроса, на котором надо заканчивать)
    """
    all_surveys = surveys = await repo.get_surveys()
    from_ = int(request.args.get("from", 0))
    to_ = int(request.args.get("to", len(all_surveys)))
    surveys = all_surveys[from_:to_]
    
    if request.args.get("sorted_by", None):
        sorted_by = request.args["sorted_by"]
        if sorted_by == "new":
            func, reverse = lambda x: x.created_on, True
        elif sorted_by == "short":
            func, reverse = lambda x: x.time_to_pass, False
        elif sorted_by == "popular":
            func, reverse = lambda x: len(x.answers), True
        surveys.sort(key=func, reverse=reverse)

    return [get_survey_json(survey) for survey in surveys]


@ConnManager.db_decorator
async def survey(repo: Repo, **kwargs):
    uuid = request.args.get("uuid", None)
    survey = await repo.get_survey_by_uuid(uuid)
    if not survey:
        return "Survey with same uuid doesn't exist", 404

    return get_survey_json(survey)


@ConnManager.db_decorator
async def delete(repo: Repo, **kwargs):
    data = request.get_json(force=True)
    await repo.delete_survey(data["uuid"], data["access_hash"])

    return {"ok"}


def register_basic():
    app.add_url_rule("/create", view_func=create, methods=["POST"]) 
    app.add_url_rule("/surveys", view_func=surveys, methods=["GET"]) 
    app.add_url_rule("/survey", view_func=survey, methods=["GET"]) 
    app.add_url_rule("/delete", view_func=delete, methods=["POST"]) 

