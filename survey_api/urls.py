#!/usr/bin/env python3
from django.urls import path
from . import views

urlpatterns = [
    path("create/<int:test_version_number>", views.create),
    path("<uuid:survey_id>/question", views.next_question),
    path("<uuid:survey_id>/answer/", views.answer),
    path("<uuid:survey_id>/result/", views.result),
    path("<uuid:survey_id>/end/", views.end),
]