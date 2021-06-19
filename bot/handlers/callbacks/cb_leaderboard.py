# -*- coding: utf-8 -*-

from asyncio import gather

from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from ..states import Page

from ...db.controller import leaderboard
from ...message_templates import Message
from ...keyboards import Keyboard


async def leaderboard_page(call: CallbackQuery):
    last_note_id = leaderboard.get_rows_count()

    try:
        note_text = (leaderboard.get_row_by_id(note_id=1)).text
    except Exception as e:
        print(f'WARN: {e}')
        note_text = ''
    text_response = 'Leaderboard. Page %s/%s\n' % (1, last_note_id) + note_text

    await gather(
        call.message.edit_text(
            text=text_response, reply_markup=Keyboard.switch_page(1, last_note_id), disable_web_page_preview=True
        ),
        Page.note_id.set()
    )


async def turn_leaderboard_page(call: CallbackQuery, state: FSMContext):
    current_note_id = (await state.get_data()).get('page')
    last_note_id = leaderboard.get_rows_count()

    if call.data == 'next':

        if len(await state.get_data()) == 0:
            current_note_id = 2

            note_text = (leaderboard.get_row_by_id(current_note_id)).text
            text_response = 'Leaderboard. Page %s/%s\n' % (current_note_id, last_note_id) + note_text

            response = call.message.edit_text(
                text=text_response, reply_markup=Keyboard.switch_page(current_note_id, last_note_id),
                disable_web_page_preview=True
            )

            await gather(response, state.update_data(page=2))

        else:
            current_note_id += 1

            note_text = (leaderboard.get_row_by_id(current_note_id)).text
            text_response = 'Leaderboard. Page %s/%s\n' % (current_note_id, last_note_id) + note_text

            response = call.message.edit_text(
                text=text_response, reply_markup=Keyboard.switch_page(current_note_id, last_note_id),
                disable_web_page_preview=True
            )

            await gather(response, state.update_data(page=current_note_id))

    elif call.data == 'back':
        current_note_id -= 1

        note_text = (leaderboard.get_row_by_id(current_note_id)).text
        text_response = 'Leaderboard. Page %s/%s\n' % (current_note_id, last_note_id) + note_text

        response = call.message.edit_text(
            text=text_response, reply_markup=Keyboard.switch_page(current_note_id, last_note_id),
            disable_web_page_preview=True
        )

        await gather(response, state.update_data(page=current_note_id))

    elif call.data == 'home':
        response = call.message.edit_text(text=Message.welcome, reply_markup=Keyboard.main_menu())

        await gather(response, state.finish())


def register_leaderboard_callbacks(dp: Dispatcher):
    dp.register_callback_query_handler(
        leaderboard_page, lambda CallbackQuery: CallbackQuery.data == 'leaderboard'
    )

    dp.register_callback_query_handler(turn_leaderboard_page, state=Page.note_id)
