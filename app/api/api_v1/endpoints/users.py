from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models, crud, schemas
from app.api import dependancy
import re

router = APIRouter()

email_pattern = r'[_A-Za-z0-9-+]+(\\.[_A-Za-z09-]+)*@" + "[A-Za-z0-9-]+(\\.[A-Za-z]{2,})$'


# todo: add priveleges so that only the admin can do this
@router.get('/get_users', response_model=List[schemas.User], description='Gets all users present in the system')
def get_users(db: Session = Depends(dependancy.get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Returns a list of users present in the system
    :param db: the db session
    :param skip: skip value
    :param limit: the limit
    :return: list of users
    """
    users = crud.user.get_multiple_items(db, skip=skip, limit=limit)
    return users


@router.post('/create_user', response_model=schemas.User, description='Creates the user')
def create_user(*, db: Session = Depends(dependancy.get_db), user_in: schemas.UserCreate):
    """
    Creates and returns the newly created user
    :param db: the db session
    :param user_in: the model holding the data sent by the front end
    :return: the newly created user
    """
    user = crud.user.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail='This email is already in use')
    if len(user_in.username) <= 8 or len(user_in.username) > 30:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail='The username should be at least 8 chars '
                                   'chars less than 30 chars')
    if len(user_in.password) <= 8 or len(user_in.password) > 30:
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail='The password should be at least 8 chars '
                                   'chars less than 30 chars')
    match_ = re.match(r"[_A-Za-z0-9-+]+(\\.[_A-Za-z09-]+)*@" + "[A-Za-z0-9-]+(\\.[A-Za-z]{2,})$", string=user_in.email)
    if match_ is None:

        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='The email must be a valid email')
    else:

        if any(c.islower() for c in user_in.password) and any(c.isupper() for c in user_in.password) and any(
                c.isdigit() for c in user_in.password):
            user_in.is_active=False
            user = crud.user.create(db, obj_in=user_in)
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='The password must be a combination of '
                                       'at least a digit,an uppercase and '
                                       'lower case letter')

    # user = crud.user.create(db, obj_in=user_in)

    return user


@router.get('/current_user/me', response_model=schemas.User, description='Returns the current active user')
def get_user(current_user: models.User = Depends(dependancy.get_current_active_user)):
    """
    Returns the current active user
    :param current_user: the current active user
    :return: current active user
    """
    return current_user


@router.get('/get_user_by_id/{user_id}', response_model=schemas.User,
            description='Returns a user associated with the given id')
def get_user_by_id(user_id: int, db: Session = Depends(dependancy.get_db),
                   current_user: models.User = Depends(dependancy.get_current_user)):
    """
    Returns the user associated with the given user id
    :param user_id: the user id
    :param db: db session/connection
    :param current_user: current user
    :return: the user
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    elif not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user with this user id')
    return user


@router.get('/get_user_by_username{username}', response_model=schemas.User,
            description='Get a user by his/her username')
def get_user_by_username(username: str, db: Session = Depends(dependancy.get_db)):
    user = crud.user.get_user_by_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user with this username')

    return user


@router.delete('/delete_user/{user_id}', response_model=schemas.User,
               description='Delete the current user.Should be used with caution')
def delete_user(user_id: int, db: Session = Depends(dependancy.get_db),
                current_user: models.User = Depends(dependancy.get_current_active_user)):
    """
    Deletes the user associated with the given id
    :param user_id:
    :param db:
    :param current_user:
    :return:
    """
    user = crud.user.get(db, user_id)
    if user:
        if user == current_user:
            crud.user.remove(db=db, id=user_id)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You can only delete you')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='There is no user associated with that id')

    return user


@router.put('/update_user/current_user', response_model=schemas.User)
def update_user(*, db: Session = Depends(dependancy.get_db), password: str = Body(None)
                , username: str = Body(None), email=Body(None),
                current_user: models.User = Depends(dependancy.get_current_active_user)):
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)

    if password is not None:
        if any(c.islower() for c in user_in.password) and any(c.isupper() for c in user_in.password) and any(
                c.isdigit() for c in user_in.password):
            user_in.password = password
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='The password must be a combination of '
                                       'at least a digit,an uppercase and '
                                       'lower case letter')
    if username is not None:
        if len(user_in.username) <= 8 or len(user_in.username) > 30:
            raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                                detail='The username should be at least 8 chars '
                                       'chars less than 30 chars')
        else:
            user_in.username = username

    if email is not None:
        user_in.email = email
    user = crud.user.update(db=db, db_obj=current_user, obj_in=user_in)
    return user
