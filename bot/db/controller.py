# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .methods import wrapped_methods
from .models import wrapped_models

from config import DATABASE_PATH


base = declarative_base()
engine = create_engine(r'sqlite:///%s' % DATABASE_PATH, echo=True)
session = sessionmaker(bind=engine)()

wrapped_models = wrapped_models(base)

validator_temporary, validator_static, leaderboard = wrapped_methods(wrapped_models, session)


if not os.path.exists(DATABASE_PATH):
    base.metadata.create_all(engine)

