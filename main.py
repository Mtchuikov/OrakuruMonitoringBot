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
from aiogram.utils.markdown import *
import multiprocessing


TGBOTTOKEN = '1772648354:AAHY2m9QBzXtGVCmzPrdDSCABGjG22hyIz8'



bot = Bot(
    token=TGBOTTOKEN,
    parse_mode=types.ParseMode.HTML
)
dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage()
)

def leaderboard():
    counter, text = 0, ''

    for row in get_all_rows(ValidatorsInfo):
        counter += 1

        address = row.address[0:4] + '...' + row.address[-5:-1]

        text = text + (
                validator_stats % (counter, address, row.score,
                                  row.responses, round(row.response_time, 2))
        )
        if counter % 3 == 0:
            add_leaderboard_note(text)
            text = ''


@dp.message_handler(commands=['start'])
async def show_main_menu(message: types.Message):
    # json = await request_get(
    #     url='https://leaderboard.orakuru.io/stats',return_json=True
    # )
    # add_validator_stats_note(json)
    await message.answer(
        text=welcome_message, reply_markup=main_menu
    )


@dp.callback_query_handler(lambda CallbackQuery: CallbackQuery.data == 'show_leaderboard')
async def show_validator(call: CallbackQuery):
    message = call.message

    note = (get_row_by_id(table=PrintLeaderboard,note_id=1)).text

    await gather(
        message.edit_text(
            text=note, reply_markup=switch_leaderboard_next_page
        ),
        Page.note_id.set()
    )

@dp.callback_query_handler(state=Page.note_id)
async def switch_leaderboard_page_(call: CallbackQuery, state: FSMContext):

    message = call.message
    callback_data = call.data
    note_id = (await state.get_data()).get('page')

    if callback_data == 'next_leaderboard_page':

        if len(await state.get_data()) == 0:
            note_id = 2
            note = (get_row_by_id(PrintLeaderboard, note_id)).text

            await gather(
                message.edit_text(
                    text=note, reply_markup=switch_leaderboard_page
                ),
                state.update_data(page=2)
            )

        else:
            note_id = note_id + 1
            note = (get_row_by_id(PrintLeaderboard, note_id)).text

            if note_id == get_rows_count(PrintLeaderboard):
                keyboard = switch_leaderboard_back_page
            else:
                keyboard = switch_leaderboard_page

            await gather(
                message.edit_text(
                    text=note, reply_markup=keyboard
                ),
                state.update_data(page=note_id)
            )

    elif callback_data == 'back_leaderboard_page':
        note_id = note_id - 1
        note = (get_row_by_id(PrintLeaderboard, note_id)).text

        if note_id == 1:
            keyboard = switch_leaderboard_next_page
        else:
            keyboard = switch_leaderboard_page

        await gather(
            message.edit_text(
                text=note, reply_markup=keyboard
            ),
            state.update_data(page=note_id)
        )

    elif callback_data == 'back_to_menu':
        await gather(
            message.edit_text(
                text=welcome_message, reply_markup=main_menu
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
        EnterAddress.address.set(),
        state.update_data(message_data=message_data)
    )

@dp.callback_query_handler(state=EnterAddress)
@dp.message_handler(state=EnterAddress)
async def print_validator_stats(data: types.Message or CallbackQuery, state: FSMContext):
    if isinstance(data, CallbackQuery):
        await gather(
            data.message.edit_text(
                text=welcome_message, reply_markup=main_menu
            ),
            state.finish()
        )
    else:
        message = data
        message_ = (await state.get_data()).get('message_data')

        address = message.text
        stats = get_row_by_address(ValidatorsInfo, address)

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
