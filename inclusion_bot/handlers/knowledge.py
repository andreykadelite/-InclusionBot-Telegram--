from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command('knowledge'))
async def knowledge(message: types.Message):
    text = (
        'База знаний:\n'
        '- Горячие клавиши экранных дикторов\n'
        '- Инструкции по настройке ПО\n'
        '- Контакты службы поддержки'
    )
    await message.answer(text)
