from datetime import timedelta
from django.db import models
import uuid


class SurveyUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Survey(models.Model): 
    survey_id = models.UUIDField(default=uuid.uuid4)
    start_time = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=timedelta(hours=1))
    length = models.IntegerField()
    user = models.ForeignKey(
        'SurveyUser',
        on_delete=models.CASCADE
    )
    next_question = models.ForeignKey(
        'Question',
        on_delete=models.SET_NULL,
        null=True,
        related_name="survey_next_in"
    )


class Question(models.Model):
    qid = models.UUIDField(default=uuid.uuid4)
    source_id = models.IntegerField()
    survey = models.ForeignKey(
        'Survey',
        on_delete=models.CASCADE
    )
    text = models.TextField(max_length=500)
    submitted_option = models.ForeignKey(
        'Option',
        null=True,
        on_delete=models.SET_NULL,
        related_name="submitted_for"
    )
    correct_option = models.ForeignKey(
        'Option',
        null=True,
        on_delete=models.SET_NULL,
        related_name="correctly_answers"
    )
    position = models.IntegerField()



class Option(models.Model):
    oid = models.UUIDField(default=uuid.uuid4)
    survey = models.ForeignKey(
        'Survey',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        'Question',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=200)
    position = models.IntegerField()