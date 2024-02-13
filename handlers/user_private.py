from aiogram import types, Router, F
from aiogram.filters import Command
from reply import start_keyboard, generate_options_keyboard
from quiz_base import quiz_data
from service import get_quiz_statistic, get_quiz_index, new_statistic

user_private_router = Router()


async def show_statistic(message, results):
    await message.answer("<b>Ваша статистика за прошлую игру:</b>")
    for i, k in enumerate(quiz_data):
        await message.answer(f'<b>Вопрос:</b> {k['question']}\n'
                             f'<b>Ваш ответ:</b> <i>{quiz_data[i]['options'][int(results[i])]}</i>'

                             )


async def get_statistic(message):
    user_id = message.from_user.id
    results = await get_quiz_statistic(user_id)
    if results is not None:
        await show_statistic(message, results)
    else:
        await message.answer("У вас еще нет статистики")


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']

    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    await new_statistic(user_id)
    await get_question(message, user_id)


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
    await get_statistic(message)
