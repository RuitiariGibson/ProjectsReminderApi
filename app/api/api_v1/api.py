from fastapi import APIRouter # similar to Flask's BluePrint
from app.api.api_v1.endpoints import login, projects, users

api_router = APIRouter()
api_router.include_router(login.router, tags=['login'])
api_router.include_router(users.router, prefix='/users', tags=['users'])
api_router.include_router(projects.router, prefix='/projects', tags=['projects'])