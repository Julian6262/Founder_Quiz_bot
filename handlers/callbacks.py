from aiogram import Router, types
from service import (get_quiz_index, update_quiz_index, get_question, quiz_questions, show_result, update_result,
                     update_temp_result)

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
        await callback.message.answer("✅ Верно!")
    else:
        correct_option = quiz_questions[current_question_index][2]
        await callback.message.answer(
            f"❌ Неправильно. Правильный ответ: {quiz_questions[current_question_index][1][correct_option]}")

    await update_quiz_index(callback.from_user.id)
    await update_temp_result(callback.from_user.id, index, 1 if callback_answer == "right_answer" else 0)

    if current_question_index < len(quiz_questions) - 1:
        await get_question(callback.message, callback.from_user.id)
    else:
        await update_result(callback.from_user.id)
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await show_result(callback.message, callback.from_user.id, statistic=False)
