from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CrudBase
from app.models import User
from app.schemas import UserCreate, UserUpdate


class CrudUser(CrudBase[User, UserCreate, UserUpdate]):
    @staticmethod
    def get_user_by_email(db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(email=obj_in.email,
                      hashed_password=get_password_hash(obj_in.password), username=obj_in.username)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_user_by_username(db=db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data['password']:
            hashed_password = get_password_hash(update_data['password'])
            # delete the field password
            del update_data['password']
            # create a new field in the dict
            update_data['hashed_password'] = hashed_password
        return super().update(db=db, db_obj=db_obj, obj_in=update_data)

    @staticmethod
    def is_active(user: User) -> bool:
        return user.is_active

    def activate_user(self, db: Session, user: User):
        user.is_active = True
        db.add(user)
        db.commit()
        db.refresh(user)


user = CrudUser(User)
