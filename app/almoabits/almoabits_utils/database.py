from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.almoabits.almoabits_utils.config import settings


SQLALCHEMY_DATABASE_URL = settings.db_url

engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()