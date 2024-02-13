import aiosqlite

DB_NAME = 'quiz_bot.db'


async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY,'
                         ' question_index INTEGER, statistic TEXT, temp_statistic TEXT)')
        await db.commit()


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE quiz_state SET question_index = ? WHERE user_id = ?', (index, user_id))
        await db.commit()


async def update_statistic(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE quiz_state SET statistic = temp_statistic WHERE user_id = ?', (user_id,))
        await db.commit()


async def update_temp_statistic(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('UPDATE quiz_state SET temp_statistic = temp_statistic || ? WHERE user_id = ?',
                         (index, user_id))
        await db.commit()


async def new_statistic(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''INSERT INTO quiz_state (user_id, question_index, temp_statistic) VALUES(?, 0, '')
             ON CONFLICT(user_id) DO UPDATE SET question_index=0, temp_statistic=?''', (user_id, ''))
        await db.commit()


async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def get_quiz_statistic(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT statistic FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
