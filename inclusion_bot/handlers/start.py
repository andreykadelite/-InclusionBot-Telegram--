from aiogram import Router, types
from aiogram.filters import Command

from ..keyboards.default import main_kb
from ..database import db
from ..config import ROLE_MAP

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user = db.get_user(message.from_user.id)
    if user:
        await message.answer("Добро пожаловать обратно!", reply_markup=main_kb)
    else:
        await message.answer("Здравствуйте! Пройдите регистрацию командой /register")
