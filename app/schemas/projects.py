from pydantic import BaseModel


# base class to be inherited
class ProjectBase(BaseModel):
    project_name:str = None
    project_description:str = None
    project_completed:bool = False


class ProjectCreate(ProjectBase):
    project_name: str


class ProjectUpdate(ProjectBase):
    id:int
    project_completed:bool
    project_name:str
    owner_id:int


# prop shared by models in db
class ProjectInDbBase(ProjectBase):
    id: int
    project_name: str
    project_description: str
    project_completed: bool
    owner_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'project_name': 'Test project name',
                'project_description': 'Project test description',
                'completed': True,
                'owner_id': 1
            }
        }


# exposed to the user
class Projects(ProjectInDbBase):
    pass


# stored in db
class ProjectsInDb(ProjectInDbBase):
    pass
