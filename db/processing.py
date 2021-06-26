# -*- coding: utf-8 -*-

import asyncio

from config import *
from message_template import *
from web import *
from .controller import *

__all__ = [
    'update_data'
]


async def update_validator_table():
    for data_dict in await request_get(Config.api_get_stats, return_json=True):
        selection_criteria = {'address': data_dict['address']}

        if not await validator_data.get_row_by_criteria(
                criteria=selection_criteria
        ):
            await validator_data.paste_row(data_dict)

        else:
            await validator_data.update_row_by_criteria(criteria=selection_criteria, values=data_dict)

    await validator_data.commit()


async def update_leaderboard_table():
    await leaderboard.delete_all_rows()

    note = ''
    for counter, data in enumerate(await validator_data.get_all_rows(), start=1):

        short_address = data[0].address[0:4] + '...' + data[0].address[-5:-1]
        score = data[0].score
        responses = data[0].responses
        response_time = round(data[0].response_time, 2)

        note += MessageTemplate.leaderboard_text.substitute(
            address=short_address,
            score=score,
            responses=responses,
            response_time=response_time
        )

        if counter % 3 == 0:
            await leaderboard.paste_row({'text': note})
            note = ''

    await leaderboard.commit()


async def update_data():
    while True:
        await create_database()
        await update_validator_table()
        await update_leaderboard_table()
        await asyncio.sleep(120)
