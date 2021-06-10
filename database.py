import os
import re
from sqlalchemy import (Column, String, Integer, 
                        Float, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only, sessionmaker
from config import DATABASE_NAME


class TableMethods:

    def __init__(self, Table: object, session: sessionmaker):
        self.__session = session
        self.__query = self.__session.query(Table)

    def paste_row(self, **fields):
        session.add(self.__table(**fields))
        session.commit()

    def delete_all_rows(self):
        self.__query.delete()
        self.__session.commit()

    def delete_row_by_address(self, address: str):
        self.__query.filter_by(address=address).delete()
        self.__session.commit()

    def get_all_rows(self) -> tuple:
        return self.__query.all()

    def get_row_by_address(self, address: str) -> (object or None):
        return self.__query.filter_by(address=address).first()

    def get_row_by_id(self, note_id: int) -> (object or None):
        return self.__query.get(note_id)

    def get_rows_count(self) -> int:
        return self.__query.count()


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


engine = create_engine('sqlite:///%s' %DATABASE_NAME, echo=True)
session = sessionmaker(bind=engine)()


validator_temportary_table = TableMethods(ValidatorTemportaryDataTable, session)
validator_static_table = TableMethods(ValidatorStaticDataTable, session)
leaderboard_table = TableMethods(LeaderboardTable, session)


if not os.path.exists(DATABASE_NAME):
    Base.metadata.create_all(engine)
    
