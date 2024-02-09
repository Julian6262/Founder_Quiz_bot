import asyncio
# import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from handlers.callbacks import callback_router
from handlers.user_private import user_private_router
from sqlite.quiz_base import create_table

# logging.basicConfig(level=logging.INFO)

API_TOKEN = '6017408577:AAGxA4W1awhYPJoW8iUSVug3C5GvqldTQsM'

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
dp.include_routers(user_private_router, callback_router)


async def main():
    # await create_table()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
