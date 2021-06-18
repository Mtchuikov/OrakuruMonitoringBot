# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker


def wrapped_methods(wrapped_models: tuple, wrapped_username_models: tuple, session: sessionmaker()) -> list:
    return [Methods(model, session) for model in wrapped_models] +\
           [MethodsWithUsername(model, session) for model in wrapped_username_models]


class Methods:


    def __init__(self, model: object(), session: sessionmaker()):
        self.__model = model
        self.__session = session
        self.__query = self.__session.query(model)


    def commit(self):
        self.__session.commit()


    def paste_row(self, **fields):
        self.__session.add(self.__model(**fields))


    def paste_all_rows(self, fields):
        self.__session.add_all(fields)


    def delete_all_rows(self):
        self.__query.delete()


    def delete_row_by_address(self, address: str) -> int:
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