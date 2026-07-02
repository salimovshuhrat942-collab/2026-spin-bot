# states.py

from aiogram.fsm.state import State, StatesGroup


class WithdrawStates(StatesGroup):
    waiting_game_id = State()
