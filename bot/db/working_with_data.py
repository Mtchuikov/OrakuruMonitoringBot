# -*- coding: utf-8 -*-

import asyncio

from .controller import leaderboard, validator_temporary

from ..message_templates import LeaderboardNote
from ..network_methods import request_get


async def update_temporary_data():
    while True:
        validator_temporary.delete_all_rows()

        json_answer = await request_get('https://leaderboard.orakuru.io/stats', return_json=True)

        for json_string in json_answer:
            validator_temporary.paste_row(
                address=json_string['address'], score=json_string['score'],
                response_time=json_string['response_time'], responses=json_string['responses']
            )

        validator_temporary.commit()

        counter = 0
        text = ''

        leaderboard.delete_all_rows()

        for row in validator_temporary.get_all_rows():
            counter += 1

            short_address = row.address[0:4] + '...' + row.address[-5:-1]
            text = text + LeaderboardNote % (counter, row.address ,short_address, row.score, row.responses, round(row.response_time, 2))

            if counter % 3 == 0:
                print(text)
                leaderboard.paste_row(text=text)
                text = ''

        leaderboard.commit()

        await asyncio.sleep(120)