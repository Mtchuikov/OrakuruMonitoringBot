# -*- coding: utf-8 -*-

from aiogram import Dispatcher
from aiogram.types import Message

from bot.ans_templates import WelcomeMessage
from bot.keyboards import MainMenuKeyboard


async def cmd_start(message: Message):
    await message.answer(text=WelcomeMessage, reply_markup=MainMenuKeyboard)


def register_start_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
