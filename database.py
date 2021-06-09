import os
from sqlalchemy import (Column, String, Integer, 
                        Float, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_NAME


def paste_row(table, **fields):
    session.add(table(**fields))
    session.commit()


def delete_rows(table: object):
    session.query(table).delete()
    session.commit()


def get_all_rows(table: object) -> tuple:
    return session.query(table).all()


def get_row_by_address(table: object, address: str) -> (object or None):
    return session.query(table).filter_by(address=address).first()


def get_row_by_id(table: object, note_id: int) -> (object or None):
    return session.query(table).get(note_id)


def get_rows_count(table: object) -> int:
    return session.query(table).count()


def add_validator_stats_note(json_response: list) -> None:
    table = ValidatorDataTable

    if get_rows_count(table) != 0:
        delete_rows(table)

    for json_string in json_response:
        paste_row(
            ValidatorDataTable,
            address=json_string['address'],
            score=json_string['score'],
            response_time=json_string['response_time'],
            responses=json_string['responses']
        )


Base = declarative_base()

class ValidatorDataTable(Base):
    __tablename__ = 'validator_data_temporary'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column('address', String)
    score = Column(Integer)
    response_time = Column(Float)
    responses = Column(Integer)


class LeaderboardTable(Base):
    __tablename__ = 'leaderboard'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)


engine = create_engine('sqlite:///%s' %DATABASE_NAME)
session = sessionmaker(bind=engine)()


if not os.path.exists(DATABASE_NAME):
    Base.metadata.create_all(engine)
