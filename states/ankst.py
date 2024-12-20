from aiogram.fsm.state import StatesGroup, State


class newAnketa(StatesGroup):
    name = State()
    phone = State()
    job = State()
    goal = State()
