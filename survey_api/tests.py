import json
from django.test import TestCase
from django.urls import reverse

from .views import (
    create,
    answer,
    next_question,
)


class TestViews(TestCase):
    def test_survey_views(self):

        # Create New Survey
        response = self.client.post(
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
        response = self.client.get(
            reverse(next_question, kwargs={"survey_id": surveyid})
        )
        assert response.status_code == 200
        response_data = json.loads(response.content)
        oid = response_data["Data"]["Options"][3]['fields']['oid']
        qid = response_data["Data"]["Id"]


        # Post Correct Answer
        response = self.client.post(
            reverse(answer, kwargs={"survey_id": surveyid}),
            data={
                "QuestionID": qid,
                "OptionID": oid,
            },
        )
        assert json.loads(response.content)["Message"] == "Success"
