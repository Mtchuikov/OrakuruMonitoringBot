import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from bot.config import DATABASE_NAME


Base = declarative_base()
engine = create_engine(r'sqlite:///%s' % DATABASE_NAME, echo=True)
session = sessionmaker(bind=engine)()

if not os.path.exists(DATABASE_NAME):
    Base.metadata.create_all(engine)