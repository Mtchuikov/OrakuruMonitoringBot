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


TGBOTTOKEN = '1772648354:AAHY2m9QBzXtGVCmzPrdDSCABGjG22hyIz8'


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

    for row in validator_temporary_table.get_all_rows():
        counter += 1

        address = row.address[0:4] + '...' + row.address[-5:-1]

        text = text + (
                validator_stats % (counter, address, row.score,
                                  row.responses, round(row.response_time, 2))
        )
        if counter % 3 == 0:
            print(text)
            leaderboard_table.paste_row(text=text)
            text = ''


@dp.message_handler(commands=['start'])
async def show_main_menu(message: types.Message):
    await message.answer(
        text=welcome_message, reply_markup=MainMenuKeyboard
    )


@dp.callback_query_handler(
    lambda CallbackQuery: CallbackQuery.data == 'show_leaderboard'
)
async def show_leaderboard_page(callback: CallbackQuery):
    note_text = (leaderboard_table.get_row_by_id(note_id=1)).text

    await gather(
        callback.message.edit_text(
            text=note_text, reply_markup=TurnLeaderboardPageKeyboard(1)
        ),
        statePage.note_id.set()
    )
    

@dp.callback_query_handler(state=statePage.note_id)
async def turn_leaderboard_page(callback: CallbackQuery, state: FSMContext):
    current_note_id = (await state.get_data()).get('page')
    last_note_id = leaderboard_table.get_rows_count()

    if callback.data == 'next_leaderboard_page':

        if len(await state.get_data()) == 0:
            current_note_id = 2
            note_text = (leaderboard_table.get_row_by_id(current_note_id)).text

            await gather(
                callback.message.edit_text(
                    text=note_text, reply_markup=TurnLeaderboardPageKeyboard(current_note_id, last_note_id)
                ),
                state.update_data(page=2)
            )

        else:
            current_note_id += 1
            note_text = (leaderboard_table.get_row_by_id(current_note_id)).text

            await gather(
                callback.message.edit_text(
                    text=note_text, reply_markup=TurnLeaderboardPageKeyboard(current_note_id, last_note_id)
                ),
                state.update_data(page=current_note_id)
            )

    elif callback.data == 'back_leaderboard_page':
        current_note_id -= 1
        note_text = (leaderboard_table.get_row_by_id(current_note_id)).text

        await gather(
            callback.message.edit_text(
                text=note_text, reply_markup=TurnLeaderboardPageKeyboard(current_note_id, last_note_id)
            ),
            state.update_data(page=current_note_id)
        )

    elif callback.data == 'back_to_menu':
        await gather(
            callback.message.edit_text(
                text=welcome_message, reply_markup=MainMenuKeyboard
            ),
            state.finish()
        )


@dp.callback_query_handler(
    lambda CallbackQuery: CallbackQuery.data in ['check_validator', 'try_find_validator_again']
)
async def check_validator(callback: CallbackQuery, state: FSMContext):
    message_data = await callback.message.edit_text(
        text="Paste validator's address", reply_markup=BackHomeKeyboard
    )

    await gather(
        stateEnterAddress.address.set(),
        state.update_data(message_data=message_data)
    )


@dp.callback_query_handler(state=stateEnterAddress)
@dp.message_handler(state=stateEnterAddress)
async def show_validator_stats(data: types.Message or CallbackQuery, state: FSMContext):
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
        stats = validator_temporary_table.get_row_by_address(address)

        if not stats:
            await gather(
                message.delete(),
                message_.edit_text(text=no_data % address,
                                   reply_markup=SearchValidatorAgainKeyboard)
            )

        else:
            address = address[0:4] + '...' + address[-5:-1]
            rank, score, response_time, responses = stats.id, stats.score, stats.response_time, stats.responses

            await gather(
                message.delete(),
                message_.edit_text(
                    text=validator_stats % (rank, address, score,
                                            responses, round(response_time, 2)),
                    reply_markup=BackHomeKeyboard
                )
            )

        await state.finish()


executor.start_polling(dp, skip_updates=True)
