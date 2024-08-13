from os import getenv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

engine = create_engine(getenv('URI'))

Base = declarative_base()

session_local = sessionmaker(bind=engine)

def conn_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()