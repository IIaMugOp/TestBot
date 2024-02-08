from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_wait() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Отменить вопрос")
    kb.button(text='Посмотреть текущий вопрос')
    kb.button(text='Главное меню')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)