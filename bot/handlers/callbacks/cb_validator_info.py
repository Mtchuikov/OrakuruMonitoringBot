# -*- coding: utf-8 -*-

from asyncio import gather

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from ..states import SetValidatorAddress

from ...db.controller import validator_static, validator_by_user_id
from ...keyboards import Keyboard
from ...message_templates import message


async def check_validator(call: CallbackQuery, state: FSMContext):
    if call.data == 'home':
        await gather(
            state.finish(), call.message.edit_text(text=message.welcome, reply_markup=Keyboard.main_menu())
        )
    else:
        try:
            user_id = call.from_user['id']
        except Exception as e:
            print(f'WARN: {e}')
            user_id = None
        row_with_address = validator_by_user_id.get_row_by_criteria({'user_id': user_id})

        if call.data == 'repeat' and row_with_address:
            row_with_address = None
            validator_by_user_id.delete_row_by_criteria({'user_id': user_id})

        if not row_with_address:
            call_data = await call.message.edit_text(
                text=message.ask_address, reply_markup=Keyboard.home()
            )
            await gather(
                SetValidatorAddress.address.set(), state.update_data(message_data=call_data)
            )

        else:
            await show_validator_stats(call, state)


def generate_response(address, stats, call_):
    short_address = address[0:4] + '...' + address[-5:-1]

    rank, score, response_time, responses = stats.id, stats.score, stats.response_time, stats.responses

    response = call_.edit_text(
        text=message.validator_statistic % (rank, address, short_address, score, responses, round(response_time, 2)),
        reply_markup=Keyboard.repeat(), disable_web_page_preview=True
    )

    return response


async def show_new_validator(call: Message or CallbackQuery, state: FSMContext):
    if isinstance(call, CallbackQuery):
        response = call.message.edit_text(text=message.welcome, reply_markup=Keyboard.main_menu())

        await gather(response, state.finish())

    else:
        call_: CallbackQuery.message = (await state.get_data()).get('message_data')

        address = call.text
        stats = validator_static.get_row_by_criteria({'address': address})
        print(stats)

        if not stats:
            response = call_.edit_text(text=message.validator_not_found, reply_markup=Keyboard.repeat())

            await gather(call.delete(), response)

        else:
            response = generate_response(address, stats, call_)
            validator_by_user_id.paste_row({
                'user_id': call_['chat']['id'], 'address': address
            })
            validator_by_user_id.commit()

            await gather(call.delete(), response)


async def show_validator_stats(call: Message or CallbackQuery, state: FSMContext):
    call_: CallbackQuery.message = (await state.get_data()).get('message_data')
    print(call_)
    user_id = call.from_user['id']

    row_with_address = validator_by_user_id.get_row_by_criteria({'user_id': user_id})
    if not row_with_address:
        await show_new_validator(call, state)
    else:
        address = row_with_address.address
        stats = validator_static.get_row_by_criteria({'address': address})
        if call_:
            response = generate_response(address, stats, call_)
            await gather(call.delete(), response)
        else:
            response = generate_response(address, stats, call.message)
            await gather(response)
    await state.finish()


def register_validator_callback(dp: Dispatcher):
    dp.register_callback_query_handler(
        check_validator, lambda CallbackQuery: CallbackQuery.data in [
            'find_validator', 'repeat', 'home'
        ]
    )

    dp.register_message_handler(show_validator_stats, state=SetValidatorAddress)
    dp.register_callback_query_handler(show_validator_stats, state=SetValidatorAddress)
