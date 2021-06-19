# -*- coding: utf-8 -*-

from aiogram import Dispatcher
from aiogram.types import Message

from ...message_templates import Message
from ...keyboards import Keyboard


async def cmd_start(message: Message):
    await message.answer(text=Message.welcome, reply_markup=Keyboard.main_menu())


def register_start_cmd(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
