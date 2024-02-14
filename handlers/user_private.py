from aiogram import types, Router, F
from aiogram.filters import Command
from reply import start_keyboard
from service import new_quiz, get_statistic

user_private_router = Router()


@user_private_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=start_keyboard)


@user_private_router.message(F.text == "Начать игру")
@user_private_router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)


@user_private_router.message(F.text == "Вывести статистику")
@user_private_router.message(Command("statistic"))
async def cmd_quiz(message: types.Message):
    await get_statistic(message, message.from_user.id, statistic=True)
