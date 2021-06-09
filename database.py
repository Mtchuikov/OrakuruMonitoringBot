import os
from re import T
from sqlalchemy import (Column, String, Integer, 
                        Float, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_NAME


def paste_row(table, **fields):
    session.add(table(**fields))
    session.commit()


def delete_all_rows(table: object):
    session.query(table).delete()
    session.commit()


def delete_row_by_address(table: object, address: str):
    session.query(table).filter_by(address=address).delete()


def get_all_rows(table: object) -> tuple:
    return session.query(table).all()


def get_row_by_address(table: object, address: str) -> (object or None):
    return session.query(table).filter_by(address=address).first()


def get_row_by_id(table: object, note_id: int) -> (object or None):
    return session.query(table).get(note_id)


def get_rows_count(table: object) -> int:
    return session.query(table).count()


def add_validator_stats_note(json_response: list) -> None:
    table = ValidatorTemportaryDataTable

    if get_rows_count(table) != 0:
        delete_all_rows(table)

    for json_string in json_response:
        paste_row(
            ValidatorTemportaryDataTable,
            address=json_string['address'],
            score=json_string['score'],
            response_time=json_string['response_time'],
            responses=json_string['responses']
        )


Base = declarative_base()

class ValidatorTemportaryDataTable(Base):
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
    comission = Column(Integer)

    total_score = Column(Integer)
    daily_score_changes = Column(Integer)
    weekly_score_changes = Column(Integer)
    monthly_score_changes = Column(Integer)

    current_response_time = Column(Float)
    avarage_response_time = Column(Float)

    total_stake = Column(Float)
    daily_stake_changes = Column(Float)
    weekly_stake_changes = Column(Float)
    monthly_stake_changes = Column(Float)
    
class LeaderboardTable(Base):
    __tablename__ = 'leaderboard'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)


engine = create_engine('sqlite:///%s' %DATABASE_NAME)
session = sessionmaker(bind=engine)()


if not os.path.exists(DATABASE_NAME):
    Base.metadata.create_all(engine)