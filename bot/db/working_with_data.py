# -*- coding: utf-8 -*-

import asyncio

from bot.network_methods import request_get
from bot.ans_templates import LeaderboardNote

from .table_methods import temporary_data, leaderboard


async def update_temporary_data():
    while True:
        temporary_data.delete_all_rows()

        json_answer = await request_get('https://leaderboard.orakuru.io/stats', return_json=True)

        for json_string in json_answer:
            temporary_data.paste_row(
                address=json_string['address'], score=json_string['score'],
                response_time=json_string['response_time'], responses=json_string['responses']
            )

        temporary_data.commit()

        counter = 0; text = ''

        leaderboard.delete_all_rows()

        for row in temporary_data.get_all_rows():
            counter += 1

            short_address = row.address[0:4] + '...' + row.address[-5:-1]
            text = text + LeaderboardNote % (counter, row.address ,short_address, row.score, row.responses, round(row.response_time, 2))

            if counter % 3 == 0:
                print(text)
                leaderboard.paste_row(text=text)
                text = ''

        temporary_data.commit()

        await asyncio.sleep(120)

# async def make_leaderboard_text_entry():