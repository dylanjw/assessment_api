# Assessment Survey API

Requires python 3.9 or above

To set up your environment:

```bash
# set up a virtual environment
python -m venv venv
. venv/bin/activate
pip install poetry
poetry install
./manage.py migrate
```

Running tests:

```bash
pytest
```

Starting the dev server:

```bash
./manage.py runserver
```

### Endpoints

**POST** `api/v1/create/{TestVersion}`

`TestVersion` is an integer representing the which set of test questions to show. At the moment there is only a single set with a single question. For now just use a value of `0`.

**Parameters**
`Name`
`Surname`
`Email`

**Response Object**
`{"surveyid": <UUID>}`


---

**GET** `api/v1/{SurveyID}/question`

Retrieves the next question. 

*TODO: This should take a question ID and currently it does not. If questions need to be blocked from being viewed after submission, a different solution should be found.*

**Response Object**
```
{
        "Status": 1,
        "Message": "Success",
        "Data": {
            "Id": $questionID,
            "Text": $text,
            "Options": [
                { "fields": {"oid": $OptionID, "text": $text } } ...
            ],
            "RemainingSeconds": $remaining_seconds,
        },
    }
```


---

**POST** `api/v1/{SurveyID}/answer`

Submit and answer

Parameters:
`QuestionID`
`OptionID`


---

**GET** `api/v1/{SurveyID}/end`

Ends the survey, and calculates results. Results are ready after the successful response is received.


---

**GET** `api/v1/{SurveyID}/result`

Retrieve result

**Response Object**

```
{
        "Status": $status,
        "Message": $message,
        "Data": {
            "Id": $survey_id,
            "TestType": $test_type,
            "TakerId": $SurveyUserID,
            "TakerName": $name,
            "TakerSurname": $lastname,
            "TakerEmail": $email,
            "QuestionCount": $question_count,
            "AssessmentTotalScore": $score,
            "EmptyAnswers": $empty_answers,
            "CorrectAnswers": $correct_answers,
            "InCorrectAnswers": $incorrect_answers,
            "TimeTaken": $time_taken,
            "StartDate": $start_time,
            "EndDate": $end_time,
            "IpAddress": $ip_address,
        },
    }
```

---

More TODO:

- [ ] Allow for survey question file downloads
- [ ] Question categories