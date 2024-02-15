from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

start_keyboard = ReplyKeyboardBuilder()
start_keyboard.add(KeyboardButton(text='Начать игру'),
                   KeyboardButton(text='Вывести статистику'),
                   )
start_keyboard = start_keyboard.adjust(1, 1).as_markup(resize_keyboard=True, )


def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()
    for count, option in enumerate(answer_options):
        builder.add(InlineKeyboardButton(
            text=option, callback_data=f'{count} {"right_answer" if option == right_answer else "wrong_answer"}')
        )
    builder.adjust(1)
    return builder.as_markup()
