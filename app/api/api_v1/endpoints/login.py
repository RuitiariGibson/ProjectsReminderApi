from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, crud, schemas
from app.api import dependancy
from app.core import security
from app.core.config import settings


router = APIRouter()


@router.post('/login/access-token', response_model=schemas.Token)
def login_access_token(db: Session = Depends(dependancy.get_db),
                       form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = crud.user.authenticate(db=db, username=form_data.username,
                                  password=form_data.password)
    if not user:
        raise HTTPException(status_code=400,
                            detail='The username/password is incorrect')
    elif crud.user.is_active(user):
        raise HTTPException(status_code=400, detail='User is already active')
    access_token_expiry_time = timedelta(minutes=settings.access_token_expire_minutes)
    crud.user.activate_user(db=db,user=user)
    return {'access_token': security.create_access_token(user.id,
                                                         expires_delta=access_token_expiry_time),'token_type': 'bearer'}


@router.post('/login/test-token', response_model=schemas.User)
def test_token(current_user: models.User = Depends(dependancy.get_current_user)) -> Any:
    return current_user
