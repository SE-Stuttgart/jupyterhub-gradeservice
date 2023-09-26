# Gradeservice

## Setup

Install requirements (requires python 3.11):
`pip install -e '.[dev]'`

Start the api (without jwt authentication):
`NO_AUTH=true uvicorn gradeservice.main:app --reload --port 5000`

## Environment variables

```sh
NO_AUTH = false # set this to true to disable jwt authentication (use this for local testing only)
JWT SECRET = 'secret' # put your secure jwt secret here
ASSIGNMENTS_PATH = '/assignments' # path to the folder where assignments should be stored
GRADING_TIMEOUT = 120 # timeout for submission grading in seconds
```
