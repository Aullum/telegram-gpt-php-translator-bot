from aiogram.fsm.state import State, StatesGroup


class TranslateStates(StatesGroup):
    file_path = State()
    waiting_for_language = State()
