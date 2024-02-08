from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_user() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="/start")
    kb.button(text='/info')
    kb.button(text='Задать вопрос')
    kb.button(text='Статус вопроса')
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)