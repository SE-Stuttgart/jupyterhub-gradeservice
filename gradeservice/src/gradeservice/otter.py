import base64
import json
import os
import shutil
import subprocess
from pathlib import Path
from subprocess import CalledProcessError, TimeoutExpired

from fastapi import APIRouter, HTTPException, UploadFile, status

from .config import settings

router = APIRouter()


# create directory and otter assign
@router.post("/{course_id}/{activity_id}", status_code=status.HTTP_201_CREATED)
async def create_assignment(course_id: int, activity_id: int, file: UploadFile):
    path = Path(f"{settings.assignments_path}/{course_id}/{activity_id}")

    file_path = path.joinpath(file.filename)
    if file_path.suffix != ".ipynb":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The file {file.filename} is not a .ipynb file.",
        )

    try:
        os.makedirs(path)
    except OSError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Activity {course_id}/{activity_id} already exists.",
        )

    try:
        contents = await file.read()
        with open(file_path, "wb") as fp:
            fp.write(contents)

        try:
            subprocess.run(
                [f"otter assign --no-pdfs {file_path} {path}"],
                shell=True,
                capture_output=True,
                check=True,
                text=True,
            )
        except CalledProcessError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create assignment: {e.stderr}",
            )

        autograder_exists = False
        for e in path.joinpath("autograder").glob("*-autograder_*.zip"):
            autograder_exists = True
            break
        if not autograder_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create assignment: Your file does not match the Otter-Grader assignment syntax.",
            )

        # get max points for each question when creating an assignment by submitting an empty file
        try:
            subprocess.run(
                [f"otter run -a {path}/autograder/*-autograder_*.zip -o {path} empty.ipynb"],
                shell=True,
                capture_output=True,
                check=True,
                text=True,
            )
        except CalledProcessError as err:
            raise HTTPException(
                status_code=400, detail=f"Failed to submit test assignment: {err.stderr}"
            )

        # reading the results and keeping the question name, max points and total points
        with open(path.joinpath("results.json"), "r") as fp:
            results = json.load(fp)["tests"]
            points = {}
            total_points, i = 0, 1
            for test_case in results:
                if "max_score" in test_case:
                    points[i] = test_case["max_score"]
                    total_points += test_case["max_score"]
                    i += 1

        with open(path.joinpath("student", file.filename), "rb") as fp:
            s = base64.b64encode(fp.read())
    except (OSError, HTTPException):
        shutil.rmtree(path)
        raise

    return {file.filename: s, "total": total_points, "points": points}


@router.post("/{course_id}/{activity_id}/{student_id}")
async def submit_upload_file(course_id: int, activity_id: int, student_id: str, file: UploadFile):
    path = Path(f"{settings.assignments_path}/{course_id}/{activity_id}")

    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Activity {course_id}/{activity_id} doesn't exist.",
        )

    submission_path = path.joinpath("submissions", student_id)
    if submission_path.exists():
        shutil.rmtree(submission_path)
    os.makedirs(submission_path)

    content = await file.read()
    submission_file_path = submission_path.joinpath(file.filename)
    with open(submission_file_path, mode="wb") as f:
        f.write(content)

    try:
        subprocess.run(
            [
                f"otter run -a {path}/autograder/*-autograder_*.zip -o {submission_path} -v {submission_file_path}"
            ],
            shell=True,
            capture_output=True,
            check=True,
            text=True,
            timeout=settings.grading_timeout,
        )
    except CalledProcessError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to grade assignment: {e.stderr}",
        )
    except TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Notebook grading timed out."
        )

    with open(f"{submission_path}/results.json", "r") as f:
        results = json.load(f)["tests"]

    score, output = {}, {}
    total_score, i = 0, 1
    for test_case in results:
        if "max_score" in test_case:
            score[i] = test_case["score"]
            output[i] = test_case["output"]
            total_score += test_case["score"]
            i += 1

    return {"total": total_score, "points": score, "output": output}


# delete assignment directory
@router.delete("/{course_id}/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_assignment(course_id: int, activity_id: int):
    path = Path(f"{settings.assignments_path}/{course_id}/{activity_id}")
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The assignment you tried to delete does not exist.",
        )
