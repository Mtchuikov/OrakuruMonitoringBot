# -*- coding: utf-8 -*-

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard:

    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton(text='🌸 Sakura', callback_data='leaderboard'),
            InlineKeyboardButton(text='🔎 Check validator', callback_data='find_validator')
        )

        return keyboard

    @staticmethod
    def home():
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(InlineKeyboardButton(text='🏠', callback_data='home'))

        return keyboard

    @staticmethod
    def switch_page(note_id: int, last_note_id: int) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=2)

        if note_id == 1:
            keyboard.add(InlineKeyboardButton(text='➡', callback_data='next'))

        elif note_id == last_note_id:
            keyboard.add(InlineKeyboardButton(text='⬅', callback_data='back'))

        else:
            keyboard.add(
                InlineKeyboardButton(text='⬅', callback_data='back'),
                InlineKeyboardButton(text='➡', callback_data='next')
            )

        keyboard.add(InlineKeyboardButton(text='🏠', callback_data='home'))

        return keyboard

    @staticmethod
    def repeat():
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton(text='🔄', callback_data='repeat'),
            InlineKeyboardButton(text='🏠', callback_data='home')
        )

        return keyboard


keyboard = Keyboard()
