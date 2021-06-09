import os
from sqlalchemy import (Table, Column, MetaData, String, 
                        Integer, Float, create_engine)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import mapper
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
    table = ValidatorsInfo

    if get_rows_count(table) != 0:
        delete_rows(table)

    for json_string in json_response:
        paste_row(
            ValidatorsInfo,
            address=json_string['address'],
            score=json_string['score'],
            response_time=json_string['response_time'],
            responses=json_string['responses']
        )


metadata = MetaData()

validators_info = Table('validators_info', metadata,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('address', String),
                        Column('score', Integer),
                        Column('response_time', Float),
                        Column('responses', Integer)
                        )

print_leaderboard = Table('print_leaderboard', metadata,
                          Column('id', Integer, primary_key=True, autoincrement=True),
                          Column('text', String)
                          )



class ValidatorsInfo(object):

    def __init__(
            self, address, score, response_time, responses
    ):
        self.address = address
        self.score = score
        self.response_time = response_time
        self.responses = responses

class PrintLeaderboard(object):

    def __init__(self, text):
        self.text = text


mapper(ValidatorsInfo, validators_info)
mapper(PrintLeaderboard, print_leaderboard)


engine = create_engine('sqlite:///%s' %DATABASE_NAME)
session = sessionmaker(bind=engine)()


if not os.getcwd() + '\\%s' %DATABASE_NAME in os.listdir():
    metadata.create_all(engine)
