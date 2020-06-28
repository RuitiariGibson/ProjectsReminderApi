import secrets
from pydantic import BaseSettings


class Settings(BaseSettings):
    api_v1_str: str = '/api/v1'
    secret_key = secrets.token_urlsafe(32)
    # random url safe string
    # 60 mins * 24 hrs * 8 days
    access_token_expire_minutes: int = 60 * 24 * 8

    # use this if you want to use sqlite rather than a server based db
    SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
    project_name: str = 'project_reminder'

    class Config:
        case_insesitive = True


settings = Settings()
