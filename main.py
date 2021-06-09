import asyncio
from asyncio import gather
from database import *
from aiogram import Bot, Dispatcher, types, executor
from network_methods import *
from keyboards import *
from answer_templates import  *
from aiogram.types.callback_query import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import *


TGBOTTOKEN = ''


bot = Bot(
    token=TGBOTTOKEN,
    parse_mode=types.ParseMode.HTML
)

dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage()
)

def make_leaderboard_text_entry():
    counter, text = 0, ''

    for row in get_all_rows(ValidatorTemportaryDataTable):
        counter += 1

        address = row.address[0:4] + '...' + row.address[-5:-1]

        text = text + (
                validator_stats % (counter, address, row.score,
                                  row.responses, round(row.response_time, 2))
        )
        if counter % 3 == 0:
            paste_row(LeaderboardTable, text)
            text = ''


@dp.message_handler(commands=['start'])
async def show_main_menu(message: types.Message):
    await message.answer(
        text=welcome_message, reply_markup=MainMenuKeyboard
    )


@dp.callback_query_handler(lambda CallbackQuery: CallbackQuery.data == 'show_leaderboard')
async def show_leaderboard_page(call: CallbackQuery):
    message = call.message

    note_text = (get_row_by_id(table=LeaderboardTable, note_id=1)).text

    await gather(
        message.edit_text(
            text=note_text, reply_markup=TurnLeaderboardPageKeyboard(1)
        ),
        statePage.note_id.set()
    )
    

@dp.callback_query_handler(state=statePage.note_id)
async def turn_leaderboard_page(call: CallbackQuery, state: FSMContext):

    message = call.message
    callback_data = call.data
    note_id = (await state.get_data()).get('page')
    last_note_id = get_rows_count(LeaderboardTable)

    if callback_data == 'next_leaderboard_page':

        if len(await state.get_data()) == 0:
            note_id = 2
            note = (get_row_by_id(LeaderboardTable, note_id)).text

            await gather(
                message.edit_text(
                    text=note, reply_markup=TurnLeaderboardPageKeyboard
                ),
                state.update_data(page=2)
            )

        else:
            note_id += 1
            note = (get_row_by_id(LeaderboardTable, note_id)).text

            await gather(
                message.edit_text(
                    text=note, reply_markup=TurnLeaderboardPageKeyboard(note_id, last_note_id)
                ),
                state.update_data(page=note_id)
            )

    elif callback_data == 'back_leaderboard_page':
        note_id -= 1
        note = (get_row_by_id(LeaderboardTable, note_id)).text

        await gather(
            message.edit_text(
                text=note, reply_markup=TurnLeaderboardPageKeyboard(note_id, last_note_id)
            ),
            state.update_data(page=note_id)
        )

    elif callback_data == 'back_to_menu':
        await gather(
            message.edit_text(
                text=welcome_message, reply_markup=Main
            ),
            state.finish()
        )


@dp.callback_query_handler(lambda CallbackQuery: CallbackQuery.data in ['check_validator', 'try_again'])
async def check_validator(call: CallbackQuery, state: FSMContext):
    message = call.message

    message_data = await message.edit_text(
        text="Paste validator's address", reply_markup=home_button
    )
    await gather(
        stateEnterAddress.address.set(),
        state.update_data(message_data=message_data)
    )


@dp.callback_query_handler(state=stateEnterAddress)
@dp.message_handler(state=stateEnterAddress)
async def print_validator_stats(data: types.Message or CallbackQuery, state: FSMContext):
    if isinstance(data, CallbackQuery):
        await gather(
            data.message.edit_text(
                text=welcome_message, reply_markup=MainMenuKeyboard
            ),
            state.finish()
        )
    else:
        message = data
        message_ = (await state.get_data()).get('message_data')

        address = message.text
        stats = get_row_by_address(ValidatorTemportaryDataTable, address)

        if not stats:
            await gather(
                message.delete(),
                message_.edit_text(text=no_data % address, reply_markup=paste_validator_address_again)
            )
        else:
            address = address[0:4] + '...' + address[-5:-1]
            rank, score, response_time, responses = stats.id, stats.score, stats.response_time, stats.responses

            await gather(
                message.delete(),
                message_.edit_text(
                    text=validator_stats % (rank, address, score,
                                            responses, round(response_time, 2)),
                    reply_markup=home_button
                )
            )

        await state.finish()


executor.start_polling(dp, skip_updates=True)
