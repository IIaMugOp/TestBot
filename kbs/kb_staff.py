from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_staff() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Количество текущих вопросов")
    #kb.button(text='Текущий вопрос')
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)