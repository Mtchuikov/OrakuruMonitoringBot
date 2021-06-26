# -*- coding: utf-8 -*-

from aiogram.types import Message
from message_template import MessageTemplate
from keyboard import *

__all__ = [
    'start'
]


async def start(message: Message):
    await message.answer(
        text=MessageTemplate.welcome,
        reply_markup=Keyboard.main_menu()
    )