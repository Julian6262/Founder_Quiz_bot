import aiosqlite
from aiogram.types import FSInputFile
from reply import generate_options_keyboard

DB_NAME = 'quiz_bot.db'
quiz_questions = []


async def select_from_questions():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_questions') as cursor:
            results = await cursor.fetchall()
            if results is not None:
                for lst in results:
                    quiz_questions.append((lst[1], lst[2].split(','), lst[3]))
            else:
                return 0


async def send_image(message, path):
    await message.answer_photo(photo=FSInputFile(path))


async def show_score(message, results):
    await message.answer("☑️ <b>Количество очков:</b> ☑️")
    await message.answer(f'<b>Вы набрали {results[1]} из {len(quiz_questions)} баллов</b>')


async def show_statistic(message, results):
    await message.answer("☑️ <b>Ваша статистика за прошлую игру:</b> ☑️")
    for i, k in enumerate(quiz_questions):
        await message.answer(f'<b>Вопрос:</b> {k[0]}\n'
                             f'<b>Ваш ответ:</b> {"✅" if int(results[0][i]) == quiz_questions[i][2] else "❌ "}'
                             f'<i>{quiz_questions[i][1][int(results[0][i])]}</i>'
                             )


async def show_result(message, user_id, statistic):
    results = await get_result(user_id)
    if results[0] is not None:
        if statistic:
            await show_statistic(message, results)
        await show_score(message, results)
    else:
        await message.answer("У вас еще нет статистики")


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_option = quiz_questions[current_question_index][2]
    opts = quiz_questions[current_question_index][1]
    kb = generate_options_keyboard(opts, opts[correct_option])
    await message.answer(f"{quiz_questions[current_question_index][0]}", reply_markup=kb)


async def new_quiz(message):
    user_id = message.from_user.id
    await new_statistic(user_id)
    await get_question(message, user_id)


async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY,'
            'question_index INTEGER, score INTEGER, temp_score INTEGER, statistic TEXT, temp_statistic TEXT)')

        await db.execute('CREATE TABLE IF NOT EXISTS quiz_questions (question_id INTEGER PRIMARY KEY,'
                         'question TEXT, options TEXT, correct_option INTEGER)')
        await db.commit()


async def update_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE quiz_state SET question_index = question_index + 1 WHERE user_id = ?', (user_id,))
        await db.commit()


async def update_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE quiz_state SET statistic = temp_statistic, score = temp_score WHERE user_id = ?', (user_id,))
        await db.commit()


async def update_temp_result(user_id, index, score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE quiz_state SET temp_statistic = temp_statistic || ?, temp_score = temp_score + ? WHERE user_id = ?',
            (index, score, user_id))
        await db.commit()


async def new_statistic(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''INSERT INTO quiz_state(user_id, question_index, score, temp_score, temp_statistic) VALUES(?, 0, 0, 0, '')
             ON CONFLICT(user_id) DO UPDATE SET question_index = 0, temp_score = 0, temp_statistic =?''', (user_id, ''))
        await db.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def get_result(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT statistic, score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results
            else:
                return 0
