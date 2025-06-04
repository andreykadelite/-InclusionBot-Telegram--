from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from ..database import db

router = Router()

class RequestForm(StatesGroup):
    text = State()

@router.message(Command('request'))
async def request_start(message: types.Message, state: FSMContext):
    await message.answer('Опишите вашу проблему:')
    await state.set_state(RequestForm.text)

@router.message(RequestForm.text)
async def request_save(message: types.Message, state: FSMContext):
    req_id = db.add_request(message.from_user.id, message.text)
    await message.answer(f'Ваша заявка #{req_id} принята.')
    await state.clear()

@router.message(Command('myrequests'))
async def my_requests(message: types.Message):
    rows = db.list_user_requests(message.from_user.id)
    if not rows:
        await message.answer('Заявок не найдено')
        return
    msg = '\n'.join([f"#{r[0]} [{r[2]}] {r[1]}" for r in rows])
    await message.answer(msg)
