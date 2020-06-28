from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, crud, schemas
from app.api import dependancy

router = APIRouter()


@router.post('/create_project', response_model=schemas.Projects)
def create_project(*, db: Session = Depends(dependancy.get_db), project_in: schemas.ProjectCreate,
                   current_user: models.User = Depends(dependancy.get_current_active_user)):
    """
    Creates a project associated with the current active user
    :param db: database connection
    :param project_in: the model holding the data
    :param current_user: the current active user
    :return: the project
    """
    project_= crud.project.get_project_by_name(db,project_in.project_name)
    if project_:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail='There exist another project with the same name.Please '
                                                             'enter a unique name')
    else:
        if project_in.project_name and project_in.project_description:
            project = crud.project.create_with_owner(db=db, obj_in=project_in, owner_id=current_user.id)
        else:
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE,detail='Project name and description cannot be blank')
    return project


@router.get('/get_projects', response_model=List[schemas.Projects])
def get_projects(db: Session = Depends(dependancy.get_db), skip: int = 0, limit: int = 100
                 , current_user: models.User = Depends(dependancy.get_current_active_user)):
    """
    Returns projects associated with the current active user
    :param db: the db connection instance
    :param skip: the skip value
    :param limit: the limit/range i.e from skip up to limit
    :param current_user: current active user
    :return: a list of projects
    """
    projects = crud.project.get_multiple_projects(db, owner_id=current_user.id, skip=skip, limit=limit)
    return projects


@router.get('/{project_id}', response_model=schemas.Projects)
def get_project(*, db: Session = Depends(dependancy.get_db), id: int,
                current_user: models.User = Depends(dependancy.get_current_active_user)):
    """
    Returns project with the given project id
    The user requesting for this project must be the owner otherwise an exception will be thrown
    :param db: db session
    :param id: project id
    :param current_user: active user/ project owner
    :return: project
    """
    project = crud.project.get(db=db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    elif not current_user.id == project.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Cannot access another persons project')

    return project


@router.delete('/{project_id}', response_model=schemas.Projects)
def delete_project(*, db: Session = Depends(dependancy.get_db), id: int,
                   current_user: models.User = Depends(dependancy.get_current_active_user)):
    """
    Deletes a project with the given id
    The project to be deleted must be associated with the current active user otherwise an exception will be thrown
    :param db: the db session
    :param id: the project id
    :param current_user: the current active user
    :return: the deleted project item
    """
    project = crud.project.get(db=db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail='Project not found')
    elif not project.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Cannot delete another persons project')
    project = crud.project.remove(db=db, id=id)
    return project
