from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings as sys

SQLALCHEMY_DATABASE_URL = f'postgresql://{sys.database_username}:{sys.database_password}@{sys.database_hostname}:{sys.database_port}/{sys.database_name}'



engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
