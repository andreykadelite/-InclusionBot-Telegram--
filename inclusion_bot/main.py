import asyncio
from aiogram import Bot, Dispatcher

from .config import TOKEN
from .handlers import start, register, request, knowledge

async def main():
    if not TOKEN:
        raise RuntimeError('TELEGRAM_TOKEN not set')
    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        register.router,
        request.router,
        knowledge.router,
    )

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
