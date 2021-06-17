# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base


def wrapped_models(Base: declarative_base):


    class ValidatorTemporary(Base):
        __tablename__ = 'validator_temporary'

        id = Column(Integer, primary_key=True, autoincrement=True)
        address = Column(String, unique=True)
        score = Column(Integer)
        response_time = Column(Float)
        responses = Column(Integer)


    class ValidatorStatic(Base):
        __tablename__ = 'validator_static'

        id = Column(Integer, primary_key=True, autoincrement=True)
        address = Column(String, unique=True)
        commission = Column(Integer)

        total_score = Column(Integer)
        daily_score_changes = Column(Integer)
        weekly_score_changes = Column(Integer)
        monthly_score_changes = Column(Integer)

        current_response_time = Column(Float)
        average_response_time = Column(Float)

        total_stake = Column(Float)
        daily_stake_changes = Column(Float)
        weekly_stake_changes = Column(Float)
        monthly_stake_changes = Column(Float)


    class Leaderboard(Base):
        __tablename__ = 'leaderboard'

        id = Column(Integer, primary_key=True, autoincrement=True)
        text = Column(String)


    return ValidatorTemporary, ValidatorStatic, Leaderboard

    