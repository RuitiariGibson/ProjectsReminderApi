from typing import List, Union, Dict, Any,Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CrudBase

from app.models import Projects
from app.schemas import ProjectCreate, ProjectUpdate





class CrudProject(CrudBase[Projects, ProjectCreate,ProjectUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: ProjectCreate,
                          owner_id: int) -> Projects:
        # first serialize the project data gotten
        serialized_data = jsonable_encoder(obj_in)
        # map the data to the model class 
        db_obj = self.model(**serialized_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Projects, obj_in: Union[ProjectUpdate, Dict[str, Any]]) -> Projects:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super(CrudProject, self).update(db=db, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def get_project_by_name(db:Session, *, project_name:str)->Optional[Projects]:
        return db.query(Projects).filter(Projects.project_name== project_name).first()

    def get_multiple_projects(self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100) -> List[Projects]:
        return db.query(self.model).filter(Projects.owner_id == owner_id).offset(skip).limit(limit).all()


project = CrudProject(Projects)
