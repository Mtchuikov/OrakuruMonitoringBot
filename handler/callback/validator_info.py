# -*- coding: utf-8 -*-

from asyncio import gather

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from db.controller import validator_data, user_state
from keyboard import *
from message_template import *

__all__ = [
    'State_validator_info',
    'check_validator',
    'show_validator',
]


class State_validator_info(StatesGroup):
    address = State()
    message_data = State()
    successfully_found = State()


async def check_validator(call: CallbackQuery, state: FSMContext):
    data = await user_state.get_row_by_criteria(criteria={'user_id': call.from_user.id})

    if data is not None:
        address = data[0].state

        data = await validator_data.get_row_by_criteria(criteria={'address': address})

        short_address = address[0:4] + '...' + address[-5:-1]

        validator_stats = MessageTemplate.validator_stats.substitute(
            address=short_address,
            score=data[0].score,
            responses=data[0].responses,
            response_time=round(data[0].response_time, 2)
        )

        message_data = await call.message.edit_text(
            text=validator_stats,
            reply_markup=Keyboard.repeat(),
            disable_web_page_preview=True
        )

    else:
        message_data = await call.message.edit_text(
            text=MessageTemplate.ask_address,
            reply_markup=Keyboard.home()
        )

    await gather(State_validator_info.address.set(), state.update_data(message_data=message_data))


async def show_validator(call: Message or CallbackQuery, state: FSMContext):
    if isinstance(call, CallbackQuery):

        if call.data == 'home':

            if (await state.get_data()).get('successfully_found') is True:
                data = (await state.get_data()).get('message_data')

                user_id = data.from_user.id
                address = data.text

                if await user_state.get_row_by_criteria(criteria={'user_id': user_id}) is None:
                    await user_state.paste_row({'user_id': user_id, 'state': address})

                else:
                    await user_state.update_row_by_criteria(criteria={'user_id':user_id}, values={'state':address})

                await user_state.commit()

            await gather(
                state.finish(),
                call.message.edit_text(text=MessageTemplate.welcome, reply_markup=Keyboard.main_menu())
            )

        else:
            message_data = await call.message.edit_text(text=MessageTemplate.ask_address, reply_markup=Keyboard.home())

            await state.update_data(message_data=message_data)

    else:
        call_ = (await state.get_data()).get('message_data')

        await state.update_data(message_data=call)

        address = call.text
        data = await validator_data.get_row_by_criteria(criteria={'address': address})

        if data is not None:
            short_address = address[0:4] + '...' + address[-5:-1]

            validator_stats = MessageTemplate.validator_stats.substitute(
                address=short_address,
                score=data[0].score,
                responses=data[0].responses,
                response_time=round(data[0].response_time, 2)
            )

            await gather(
                state.update_data(successfully_found=True),
                call.delete(),
                call_.edit_text(text=validator_stats, reply_markup=Keyboard.repeat(), disable_web_page_preview=True)
            )

        else:
            await gather(
                call.delete(),
                call_.edit_text(text=MessageTemplate.validator_not_found, reply_markup=Keyboard.repeat())
            )