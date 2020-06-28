from fastapi import FastAPI
from app.core.config import settings
from app.api.api_v1.api import api_router
from app.models import models
from app.db.session import engine

models.Base.metadata.create_all(bind=engine)

projectsapp = FastAPI(title=settings.project_name, openapi_url=f'{settings.api_v1_str}/projects_api.json')

projectsapp.include_router(api_router, prefix=settings.api_v1_str)
