# -*- coding: utf-8 -*-
import os

from .base import session, Base, engine
from .models import ValidatorTemporaryDataTable, ValidatorStaticDataTable, LeaderboardTable, UsernameNode
from ..config import DATABASE_NAME


class TableMethods:

    def __init__(self, table: object(), session=session):
        self.__table = table
        self.__session = session
        self.__query = self.__session.query(table)

    def commit(self) -> None:
        self.__session.commit()

    def paste_row(self, **fields) -> None:
        self.__session.add(self.__table(**fields))

    def paste_all_rows(self, fields) -> None:
        self.__session.add_all(fields)

    def delete_all_rows(self) -> None:
        self.__query.delete()

    def delete_row_by_address(self, address: str) -> None:
        self.__query.filter_by(address=address).delete()

    def get_all_rows(self) -> tuple:
        return self.__query.all()

    def get_row_by_address(self, address: str) -> (object or None):
        return self.__query.filter_by(address=address).first()

    def get_row_by_id(self, note_id: int) -> (object or None):
        return self.__query.get(note_id)

    def get_rows_count(self) -> int:
        return self.__query.count()


class UsernameNodeTableMethods(TableMethods):

    def __init__(self, table: object(), session=session):
        super().__init__(table, session)
        self.__table = table
        self.__session = session
        self.__query = self.__session.query(table)

    def get_row_by_username(self, username: str) -> (object or None):
        return self.__query.filter_by(username=username).first()

    def delete_row_by_username(self, username: str) -> None:
        self.__query.filter_by(username=username).delete()


if not os.path.exists(DATABASE_NAME):
    Base.metadata.create_all(engine)
static_data = TableMethods(table=ValidatorStaticDataTable)
leaderboard = TableMethods(table=LeaderboardTable)
temporary_data = TableMethods(table=ValidatorTemporaryDataTable)
username_node = UsernameNodeTableMethods(table=UsernameNode)
username_node.delete_all_rows()
username_node.commit()
