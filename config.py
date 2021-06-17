# -*- coding: utf-8 -*-

import os

from dataclasses import dataclass, field

from aiogram import Bot, Dispatcher, types


@dataclass
class Config:

    bot_token: str

    db_name: str = field(default='orakuru.db')

    def __post_init__(self):
        self.database_path = os.path.dirname(os.path.abspath(__file__)) + '\\' + self.db_name

        self.bot = Bot(self.bot_token, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot)


cfg = Config(bot_token='SET_YOUR_TOKEN')
