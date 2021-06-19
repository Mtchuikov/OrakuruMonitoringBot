# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base


def wrapped_models(Base: declarative_base):


    class ValidatorData(Base):
        __tablename__ = 'validator_static'

        id = Column(Integer, primary_key=True, autoincrement=True)
        is_active = Column(Boolean)
        address = Column(String, unique=True)

        score = Column(Integer)
        daily_score_changes = Column(Integer)
        weekly_score_changes = Column(Integer)
        monthly_score_changes = Column(Integer)

        response_time = Column(Float)
        average_response_time = Column(Float)

        responses = Column(Integer)
        daily_responses_changes = Column(Integer)
        weekly_responses_changes = Column(Integer)
        monthly_responses_changes = Column(Integer)

        current_stake = Column(Float)
        daily_stake_changes = Column(Float)
        weekly_stake_changes = Column(Float)
        monthly_stake_changes = Column(Float)


    class Leaderboard(Base):
        __tablename__ = 'leaderboard'

        id = Column(Integer, primary_key=True, autoincrement=True)
        text = Column(String)


    return ValidatorData, Leaderboard
