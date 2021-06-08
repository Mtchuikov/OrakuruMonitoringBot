from aiogram.dispatcher.filters.state import StatesGroup, State

class EnterAddress(StatesGroup):
    address = State()
    message_data = State()

class Page(StatesGroup):
    note_id = State()

class BackToMenu(StatesGroup):
    back = State()
