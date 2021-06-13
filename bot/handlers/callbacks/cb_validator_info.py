from asyncio import gather

from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.states import SetValidatorAddress
from bot.db.table_methods import temporary_data
from bot.ans_templates import WelcomeMessage, no_data, ValidatorStatistic
from bot.keyboards import BackHomeKeyboard, MainMenuKeyboard, SearchValidatorAgainKeyboard


async def check_validator(call: CallbackQuery, state: FSMContext):
    call_data = await call.message.edit_text(
        text="Paste validator's address", reply_markup=BackHomeKeyboard
    )

    await gather(
        SetValidatorAddress.address.set(), state.update_data(message_data=call_data)
    )


async def show_validator_stats(call: Message or CallbackQuery, state: FSMContext):
    if isinstance(call, CallbackQuery):
        response = call.message.edit_text(text=WelcomeMessage, reply_markup=MainMenuKeyboard)

        await gather(response, state.finish())

    else:
        call_: CallbackQuery.message = (await state.get_data()).get('message_data')

        address = call.text
        stats = temporary_data.get_row_by_address(address)

        if not stats:
            response = call_.edit_text(text=no_data % address, reply_markup=SearchValidatorAgainKeyboard)

            await gather(call.delete(), response)

        else:
            address = address[0:4] + '...' + address[-5:-1]

            rank, score, response_time, responses = stats.id, stats.score, stats.response_time, stats.responses

            response = call.edit_text(
                text=ValidatorStatistic % (rank, address, score, responses, round(response_time, 2)),
                reply_markup=BackHomeKeyboard
            )

            await gather(call.delete(), response)

        await state.finish()


def register_validator_callback(dp: Dispatcher):
    dp.register_callback_query_handler(check_validator, lambda CallbackQuery: CallbackQuery.data == 'check_validator')

    dp.register_message_handler(show_validator_stats, state=SetValidatorAddress)
    dp.register_callback_query_handler(show_validator_stats, state=SetValidatorAddress)
