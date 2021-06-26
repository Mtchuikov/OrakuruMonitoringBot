# -*- coding: utf-8 -*-

from asyncio import gather

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from db.controller import leaderboard
from keyboard import *
from message_template import *

__all__ = [
    'State_leaderboard',
    'leaderboard_page',
    'turn_leaderboard_page',
]


class State_leaderboard(StatesGroup):
    page_number = State()


async def leaderboard_page(call: CallbackQuery):
    total_pages = await leaderboard.get_rows_count()
    current_page = 1

    title = MessageTemplate.leaderboard_title.substitute(current_page=current_page, total_pages=total_pages)
    text = (await leaderboard.get_rows_offset_limit(limit=1, offset=current_page))[0].text
    print_page = title + text

    await call.message.edit_text(
        text=print_page,
        reply_markup=Keyboard.switch_page(1, total_pages),
        disable_web_page_preview=True
    )

    await State_leaderboard.page_number.set()


async def turn_leaderboard_page(call: CallbackQuery, state: FSMContext):
    total_pages = await leaderboard.get_rows_count()
    current_page = (await state.get_data()).get('page')

    if call.data == 'next':

        if len(await state.get_data()) == 0:
            current_page = 2

            title = MessageTemplate.leaderboard_title.substitute(current_page=current_page, total_pages=total_pages)
            text = (await leaderboard.get_rows_offset_limit(limit=1, offset=current_page))[0].text
            print_page = title + text

            response = call.message.edit_text(
                text=print_page,
                reply_markup=Keyboard.switch_page(current_page, total_pages),
                disable_web_page_preview=True
            )

            await gather(response, state.update_data(page=2))

        else:
            current_page += 1

            title = MessageTemplate.leaderboard_title.substitute(current_page=current_page, total_pages=total_pages)
            text = (await leaderboard.get_rows_offset_limit(limit=1, offset=current_page))[0].text
            print_page = title + text

            response = call.message.edit_text(
                text=print_page,
                reply_markup=Keyboard.switch_page(current_page, total_pages),
                disable_web_page_preview=True
            )

            await gather(response, state.update_data(page=current_page))

    elif call.data == 'back':
        total_pages = await leaderboard.get_rows_count()
        current_page -= 1

        title = MessageTemplate.leaderboard_title.substitute(current_page=current_page, total_pages=total_pages)
        text = (await leaderboard.get_rows_offset_limit(limit=1, offset=current_page))[0].text
        print_page = title + text

        response = call.message.edit_text(
            text=print_page,
            reply_markup=Keyboard.switch_page(current_page, total_pages),
            disable_web_page_preview=True
        )

        await gather(response, state.update_data(page=current_page))

    elif call.data == 'home':
        response = call.message.edit_text(
            text=MessageTemplate.welcome,
            reply_markup=Keyboard.main_menu()
        )

        await gather(response, state.finish())