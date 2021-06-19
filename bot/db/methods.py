# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session


def wrapped_methods(wrapped_models: tuple, session: Session) -> tuple:
    return [Methods(model, session) for model in wrapped_models]


class Methods:


    def __init__(self, model: object(), session: Session):
        self.__model = model
        self.__session = session
        self.__query = self.__session.query(model)


    def commit(self):
        self.__session.commit()


    def paste_all_rows(self, *rows: dict):
        self.__session.add_all(self.__model(**row) for row in rows)


    def paste_row(self, row: dict):
        self.__session.add(self.__model(**row))


    def upgrade_row_by_criteria(self, row: dict, criteria: dict):
        self.__query.filter_by(**criteria).update(row)


    def delete_all_rows(self):
        self.__query.delete()


    def delete_row_by_criteria(self, criteria: dict) -> int:
        return self.__query.filter_by(**criteria).delete()


    def get_all_rows(self) -> tuple or None:
        return self.__query.all()


    def get_row_by_criteria(self, criteria: dict) -> object or None:
        return self.__query.filter_by(**criteria).first()


    def get_rows_count(self) -> int:
        return self.__query.count()
        return self.__query.filter_by(address=address).delete()


    def get_all_rows(self) -> tuple or None:
        return self.__query.all()


    def get_row_by_address(self, address: str) -> object or None:
        return self.__query.filter_by(address=address).first()


    def get_row_by_id(self, note_id: int) -> object or None:
        return self.__query.get(note_id)


    def get_rows_count(self) -> int:
        return self.__query.count()



class MethodsWithUsername(Methods):
    def __init__(self, table: object(), session: sessionmaker()):
        super().__init__(table, session)
        self.__table = table
        self.__session = session
        self.__query = self.__session.query(table)

    def get_row_by_username(self, username: str) -> (object or None):
        return self.__query.filter_by(username=username).first()

    def delete_row_by_username(self, username: str) -> None:
        self.__query.filter_by(username=username).delete()