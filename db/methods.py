# -*- coding: utf-8 -*-

from sqlalchemy import update, delete, insert, select, func
from sqlalchemy.orm import Session

__all__ = [
    'create_methods',
]


def create_methods(models: type, session: Session) -> type:
    return [
        Methods(model, session) for model in models
    ]


class Methods:

    def __init__(self, model: object, session: Session):
        self._model = model
        self._session = session

    async def commit(self):
        await self._session.commit()

    async def close(self):
        await self._session.close()

    async def paste_row(self, row: dict):
        query = (
            insert(self._model).
                values(**row)
        )

        await self._session.execute(query)

    async def paste_all_rows(self, *rows: dict):
        query = (
            insert(self._model)
                .values(*[row for row in rows])
        )

        await self._session.execute(query)

    async def delete_row_by_criteria(self, criteria: dict):
        query = (
            delete(self._model)
                .filter_by(**criteria)
        )

        await self._session.execute(query)

    async def delete_all_rows(self):
        query = delete(self._model)

        await self._session.execute(query)

    async def update_row_by_criteria(self, criteria: dict, values: dict):
        query = (
            update(self._model)
                .filter_by(**criteria)
                .values(values)
        )

        await self._session.execute(query)

    async def get_row_by_criteria(self, criteria: dict):
        query = (
            select(self._model)
                .filter_by(**criteria)
        )

        return (await self._session.execute(query)).first()

    async def get_rows_offset_limit(self, limit: int, offset: int):
        query = (
            select(self._model)
                .limit(limit)
                .offset(offset)
        )

        execute = await self._session.execute(query)

        if limit == 1:
            return execute.first()
        else:
            return execute.all()

    async def get_all_rows(self):
        query = select(self._model)

        return (await self._session.execute(query)).all()

    async def get_rows_count(self):
        query = (
            select([func.count()])
                .select_from(self._model)
        )

        return (await self._session.execute(query)).fetchone()[0]
