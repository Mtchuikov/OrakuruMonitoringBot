from aiogram.dispatcher.filters.state import StatesGroup, State

class stateEnterAddress(StatesGroup):
    address = State()
    message_data = State()

class statePage(StatesGroup):
    note_id = State()

class stateBackToMenu(StatesGroup):
    back = State()
