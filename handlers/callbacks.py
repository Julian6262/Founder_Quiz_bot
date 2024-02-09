from aiogram import Router, types
from handlers.user_private import get_question
from quiz_data.quiz_data import quiz_data
from sqlite.quiz_base import get_quiz_index, update_quiz_index, update_temp_statistic, update_statistic

callback_router = Router()


@callback_router.callback_query()
async def answer(callback: types.CallbackQuery):
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    index, callback_answer = callback.data.split()
    await callback.message.answer(f"Ваш ответ: {callback.message.reply_markup.inline_keyboard[int(index)][0].text}")

    current_question_index = await get_quiz_index(callback.from_user.id)

    if callback_answer == "right_answer":
        await callback.message.answer("Верно!")
    else:
        correct_option = quiz_data[current_question_index]['correct_option']
        await callback.message.answer(
            f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    await update_temp_statistic(callback.from_user.id, index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await update_statistic(callback.from_user.id)
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
