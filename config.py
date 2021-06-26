# -*- coding: utf-8 -*-

from dataclasses import dataclass

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

__all__ = [
    'Config',
]


@dataclass
class Config:
    bot_token: str = 'SET_YOUR_TOKEN'

    db_password: str = 'SET_PASSWORD'
    db_user: str = 'SET_USER'
    db_host: str = 'SET_HOST'
    db_name: str = 'SET_NAME'

    api_get_stats: str = 'https://leaderboard.orakuru.io/stats'

    def __post_init__(self):
        self.connection = f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'

        self.bot = Bot(self.bot_token, parse_mode=types.ParseMode.HTML)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
