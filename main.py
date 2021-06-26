# -*- coding: utf-8 -*-

import asyncio

from aiogram import Dispatcher

from config import *
from db.processing import *
from handler.callback.leaderboard import *
from handler.callback.validator_info import *
from handler.command.start import *


async def main(dp: Dispatcher):
    dp.register_message_handler(start, commands='start')

    dp.register_callback_query_handler(leaderboard_page, lambda CallbackQuery: CallbackQuery.data == 'leaderboard')
    dp.register_callback_query_handler(turn_leaderboard_page, state=State_leaderboard.page_number)

    dp.register_callback_query_handler(check_validator, lambda CallbackQuery: CallbackQuery.data == 'check_validator')
    dp.register_callback_query_handler(show_validator, state=State_validator_info.address)
    dp.register_message_handler(show_validator, state=State_validator_info.address)

    await asyncio.gather(dp.start_polling(dp), update_data())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(Config().dp))
