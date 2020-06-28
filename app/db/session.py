from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings
# ensure each requests has its own db connection
# only needed for sqlite
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)
