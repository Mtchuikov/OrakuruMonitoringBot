# -*- coding: utf-8 -*-

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from config import *
from .methods import *
from .models import *

__all__ = [
    'validator_data',
    'leaderboard',
    'user_state',
    'create_database',
]

base = declarative_base()
engine = create_async_engine(Config().connection, echo=False)
session: Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)()

validator_data, leaderboard, user_state = create_methods(models(base), session)


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
