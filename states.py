from aiogram.fsm.state import State, StatesGroup


class Code(StatesGroup):
    name = State()
    price = State()
    description = State()
    photo = State()
    coder = State()
