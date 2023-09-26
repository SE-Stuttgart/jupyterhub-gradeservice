from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    assignments_path: Path = Path().cwd()
    no_auth: bool = False
    jwt_secret: str = ""
    grading_timeout: int = 120  # default timeout for grading is two minutes


settings = Settings()
