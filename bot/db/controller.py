# -*- coding: utf-8 -*-

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from .models import wrapped_models
from .methods import wrapped_methods

from config import cfg

base = declarative_base()
engine = create_engine(r'sqlite:///%s' % cfg.database_path)
session: Session = sessionmaker(bind=engine)()

wrapped_models = wrapped_models(base)

validator_static, leaderboard, validator_by_user_id = wrapped_methods(wrapped_models, session)

if not os.path.exists(cfg.database_path):
    base.metadata.create_all(engine)
