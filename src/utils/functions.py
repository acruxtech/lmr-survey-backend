from db.models import Survey


def get_survey_json(survey: Survey):
    res = {
        "uuid": survey.uuid,
        "title": survey.title,
        "topic": survey.topic,
        "show_result_after_passing": survey.show_result_after_passing,
    }
    if survey.after_passing_text:
        res["after_passing_text"] = survey.after_passing_text
    if survey.passing_score:
        res["passing_score"] = survey.passing_score
    if survey.time_to_pass:
        res["time_to_pass"] = survey.time_to_pass

    questions = []
    for question in survey.questions:
        q = {
            "text": question.text,
            "reward": question.reward,
            "sanction": question.sanction,
            "correct_answer": question.correct_answer,
        }

        if question.title:
            q["title"] = question.title
        if question.answers:
            q["answers"] = question.answers.split("|")
        questions.append(q)

    res["questions"] = questions
    return res
