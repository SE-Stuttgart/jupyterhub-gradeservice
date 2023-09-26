import base64
import os
from pathlib import Path

from fastapi.testclient import TestClient


def test_success(client: TestClient, testdata: Path, tmp_path: Path):
    os.chdir(tmp_path)

    with open(testdata.joinpath("demo.ipynb"), "rb") as fp:
        res = client.post("/1/2", files={"file": ("demo.ipynb", fp)})
        assert res.status_code == 201

        with open(Path("assignments/1/2/student/demo.ipynb"), "rb") as fp:
            assert base64.b64decode(res.json()["demo.ipynb"]) == fp.read()


def test_already_exists(client: TestClient, testdata: Path, tmp_path: Path):
    os.chdir(tmp_path)

    with open(testdata.joinpath("demo.ipynb"), "rb") as fp:
        res = client.post("/1/2", files={"file": ("demo.ipynb", fp)})
        assert res.status_code == 201

        res = client.post("/1/2", files={"file": ("demo.ipynb", fp)})
        assert res.status_code == 400
        assert res.json() == {"detail": "Activity 1/2 already exists."}


def test_wrong_filetype(client: TestClient, testdata: Path, tmp_path: Path):
    os.chdir(tmp_path)

    with open(testdata.joinpath("demo.ipynb"), "rb") as fp:
        res = client.post("/1/2", files={"file": ("demo.zip", fp)})
        assert res.status_code == 400
        assert res.json() == {"detail": "The file demo.zip is not a .ipynb file."}


def test_fails(client: TestClient, testdata: Path, tmp_path: Path):
    os.chdir(tmp_path)

    with open(testdata.joinpath("demo_fails.ipynb"), "rb") as fp:
        res = client.post("/1/2", files={"file": ("demo_fails.ipynb", fp)})
        assert res.status_code == 400
        # TODO: check error message

        assert not os.path.exists("assignments/1/2")
