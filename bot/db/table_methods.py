from .base import session

from .models import ValidatorTemporaryDataTable, ValidatorStaticDataTable, LeaderboardTable


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


temporary_data = TableMethods(table=ValidatorTemporaryDataTable)

static_data = TableMethods(table=ValidatorStaticDataTable)

leaderboard = TableMethods(table=LeaderboardTable)