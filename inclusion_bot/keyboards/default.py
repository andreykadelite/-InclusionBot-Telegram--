from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Паспорт доступности")],
    [KeyboardButton(text="Отправить заявку"), KeyboardButton(text="Мои заявки")],
    [KeyboardButton(text="База знаний")]
], resize_keyboard=True)
