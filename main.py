# -*- coding: utf-8 -*-

import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.commands.cmd_start import register_start_cmd
from bot.handlers.callbacks.cb_leaderboard import register_leaderboard_callbacks
from bot.handlers.callbacks.cb_validator_info import register_validator_callback
from bot.db.working_with_data import update_temporary_data

from config import TOKEN


bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    register_start_cmd(dp)
    register_leaderboard_callbacks(dp)
    register_validator_callback(dp)

    await asyncio.gather(dp.start_polling(dp), update_temporary_data())


loop = asyncio.get_event_loop()
loop.run_until_complete(main())