"""
Responsible for providing all the dependencies needed by the app
"""
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import models, crud, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

oauth_2 = OAuth2PasswordBearer(tokenUrl=f'{settings.api_v1_str}/login/access-token')


# evaluate lazily: generate it on demand only
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth_2)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[security.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Could not validate credentials')
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return user


def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail='User is not active')
    return current_user
