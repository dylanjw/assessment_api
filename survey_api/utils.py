import json
from . import models


def get_test(version_number):
    with open("questions.json", "r") as f:
        test_library = json.load(f)
    return test_library['question_sets'][version_number]


def build_test_from_config(survey, config):
    for i in range(len(config)):
        q = config[i]
        source_id = q['question_id']
        text = q['prompt']
        correct_option_id = q['correct']
        question = models.Question(
            position = i,
            source_id=source_id,
            text=text,
            survey=survey,
        )
        question.save()
        if i == 0:
            survey.next_question=question
            survey.save()
        for i in range(len(q['choices'])):
            choice = q['choices'][i]
            text = choice["text"]
            option = models.Option(
                text=text,
                survey=survey,
                question=question,
                position=i,
            )
            option.save()
            if choice["choice_id"] == correct_option_id:
                question.correct_option = option
                question.save()


def get_options(question):
    return models.Option.objects.filter(question=question).order_by('position')