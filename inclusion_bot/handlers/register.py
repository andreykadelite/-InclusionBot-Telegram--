from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from ..database import db
from ..keyboards.default import main_kb

router = Router()

class RegForm(StatesGroup):
    name = State()
    department = State()
    contact = State()
    needs = State()

@router.message(Command("register"))
async def register_start(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше ФИО:")
    await state.set_state(RegForm.name)

@router.message(RegForm.name)
async def reg_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Отдел:")
    await state.set_state(RegForm.department)

@router.message(RegForm.department)
async def reg_dept(message: types.Message, state: FSMContext):
    await state.update_data(department=message.text)
    await message.answer("E-mail или телефон:")
    await state.set_state(RegForm.contact)

@router.message(RegForm.contact)
async def reg_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Опишите особые потребности:")
    await state.set_state(RegForm.needs)

@router.message(RegForm.needs)
async def reg_needs(message: types.Message, state: FSMContext):
    data = await state.update_data(needs=message.text)
    db.add_user(
        message.from_user.id,
        data['name'],
        data['department'],
        data['contact'],
        data['needs']
    )
    await message.answer("Регистрация завершена.", reply_markup=main_kb)
    await state.clear()
