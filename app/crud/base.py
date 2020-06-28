## contains a generic class for performing the crud db operations

# TypeVar serves as a param for the generic class 
from typing import Any, Generic, Optional, Type, TypeVar, List, Union, Dict
# similar to json.dumps() serializes items  
from fastapi.encoders import jsonable_encoder
from app.db.base_class import Base
from sqlalchemy.orm import Session
from pydantic import BaseModel

# will serve as the key
ClassType = TypeVar('ClassType', bound=Base)
# will serve as the value
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CrudBase(Generic[ClassType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ClassType]):
        """
        # the model is a sqlalchemy orm class
        # the schema which will be used as an output(by our api) is pydantic model class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ClassType]:
        # get a single item
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multiple_items(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ClassType]:
        # get multiple items thus return a list of type <ClassType> 
        # *-> maintain the order of the kwargs
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ClassType:
        serialized_data = jsonable_encoder(obj_in)
        db_obj = self.model(**serialized_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ClassType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ClassType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ClassType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
