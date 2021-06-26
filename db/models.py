# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

__all__ = [
    'models',
]


def models(Base: declarative_base):

    class ValidatorStats(Base):
        __tablename__ = 'ValidatorStats'

        id = Column(Integer, primary_key=True)
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
        __tablename__ = 'Leaderboard'

        id = Column(Integer, primary_key=True)
        text = Column(String)

    class UserState(Base):
        __tablename__ = 'UserState'

        user_id = Column(Integer, primary_key=True, autoincrement=False)
        state = Column(String)

    return ValidatorStats, Leaderboard, UserState
