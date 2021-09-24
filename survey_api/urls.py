#!/usr/bin/env python3
from django.urls import path
from . import views

urlpatterns = [
    path("create/<int:test_version_number>", views.create),
    path("<uuid:survey_id>/test", views.next_question),
    path("<uuid:survey_id>/answer/", views.answer),
]