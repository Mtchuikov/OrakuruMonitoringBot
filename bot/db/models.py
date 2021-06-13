from .base import Base
from sqlalchemy import Column, String, Integer, Float


class ValidatorTemporaryDataTable(Base):
    __tablename__ = 'validator_data_temporary'

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String, unique=True)
    score = Column(Integer)
    response_time = Column(Float)
    responses = Column(Integer)


class ValidatorStaticDataTable(Base):
    __tablename__ = 'validator_data_static'

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


class LeaderboardTable(Base):
    __tablename__ = 'leaderboard'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)