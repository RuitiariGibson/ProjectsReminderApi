from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., title='Your email', description=' a valid email account')
    username: str = Field(..., title='Your username')
    is_active: bool = Field(True, title='Whether you are active or not')


class UserCreate(UserBase):
    email: str
    password: str = Field(..., title='Your password')


class UserInDbBase(UserBase):
    id: int = None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'username test',
                'email': 'test@gmail.com',
                'is_active': False,
                'password': '******'
            }
        }

    # exposed to the front end


class User(UserInDbBase):
    pass


class UserInDb(UserInDbBase):
    hashed_password: str

class UserUpdate(UserBase):
    password:Optional[str]=None