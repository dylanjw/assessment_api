import json
from datetime import timedelta
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
from .models import SurveyUser, Survey, Question, Option
from .utils import get_test, build_test_from_config, get_options
from datetime import datetime, timedelta
import pytz
from functools import wraps


def timed_survey(view_fn):
    """View function decorator for checking survey expiration
    """
    @wraps(view_fn)
    def wrap(request, survey_id, *args, **kwargs):
        try:
            survey = Survey.objects.get(survey_id=survey_id)
        except Survey.DoesNotExist:
            return HttpResponseNotFound()
        end_time = survey.start_time + survey.duration
        if datetime.now(tz=pytz.utc) > end_time:
            return HttpResponse("<h>Times Up!</h>")
        return view_fn(request, survey_id, *args, **kwargs)
    return wrap


@csrf_exempt
@require_POST
def create(request, test_version_number):
    if request.content_type == "application/json":
        data = json.loads(request.body)
    else:
        data = request.POST
    user = SurveyUser(
        first_name=data["Name"],
        last_name=data["Surname"],
        email=data["Email"],
    )
    user.save()

    test = get_test(test_version_number)
    test_length = len(test["questions"])

    survey = Survey(
        user=user, 
        length=test_length, 
    )
    survey.save()
    build_test_from_config(survey, test["questions"])

    return JsonResponse(data={"surveyid": survey.survey_id})


@timed_survey
@csrf_exempt
@require_POST
def answer(request, _):
    if request.content_type == "application/json":
        data = json.loads(request.body)
    else:
        data = request.POST
    qid = data["QuestionID"]
    oid = data["OptionID"]
    question = Question.objects.get(qid=qid)
    option = Option.objects.get(oid=oid)
    question.submitted_option=option
    question.save()
    return JsonResponse({
        "Status":1,
        "Message":"Success",
        "Data":True
    })


@timed_survey
@csrf_exempt
@require_GET
def next_question(request, survey_id):
    survey = Survey.objects.get(survey_id=survey_id)
    current = survey.next_question
    options = get_options(current)
    new_next = Question.objects.filter(
        survey=survey, 
        position__gt=current.position,
    ).order_by('position').first()
    survey.next_question = new_next
    survey.save()
    time_remaining = (
        survey.start_time 
      + survey.duration
      ) - datetime.now(tz=pytz.utc)
      
    options = json.loads(serialize(
        'json', 
        Option.objects.filter(
            survey=survey,
            question=current,
        )
    ))

    data = {
        "Status": 1,
        "Message": "Success",
        "Data": {
            "Id": current.qid,
            "Text": current.text,
            "Options": options, 
            "RemainingSeconds": time_remaining.seconds
        }
    }
    return JsonResponse(data)