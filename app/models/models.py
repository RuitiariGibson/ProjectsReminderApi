from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    projects = relationship('Projects', back_populates='owner')  # owner.proje


class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, unique=True, index=True)
    project_description = Column(String, index=True)
    project_completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='projects')  # project.owner_id
