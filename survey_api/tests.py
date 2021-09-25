import json
from django.test import TestCase
from django.urls import reverse

from .views import (
    create,
    answer,
    next_question,
    end,
    result,
)
import pytest

@pytest.mark.parametrize(
    "answer_to_select,expected_score",
    (
        (3, 100),
        (0, 0),
    )
)
@pytest.mark.django_db
def test_survey_correct_answers(
        client, 
        answer_to_select, 
        expected_score):
    # Create New Survey
    response = client.post(
        reverse(
            create,
            kwargs={"test_version_number": 0},
        ),
        data={
            "Name": "test",
            "Surname": "test",
            "Email": "test",
        },
        content_type="application/json",
    )
    assert response.status_code == 200
    response_data = json.loads(response.content)
    surveyid = response_data["surveyid"]

    # Get First Question
    response = client.get(
        reverse(next_question, kwargs={"survey_id": surveyid})
    )
    assert response.status_code == 200
    response_data = json.loads(response.content)
    oid = response_data["Data"]["Options"][answer_to_select]['fields']['oid']
    qid = response_data["Data"]["Id"]


    # Post Answer
    response = client.post(
        reverse(answer, kwargs={"survey_id": surveyid}),
        data={
            "QuestionID": qid,
            "OptionID": oid,
        },
    )
    assert json.loads(response.content)["Message"] == "Success"

    # Submit/End Survey
    response = client.post(
        reverse(end, kwargs={"survey_id": surveyid}),
    )
    assert response.status_code == 200

    # Retrieve Results
    response = client.post(
        reverse(result, kwargs={"survey_id": surveyid}),
    )
    response_data = json.loads(response.content)
    assert response_data["Data"]["AssessmentTotalScore"] == expected_score
