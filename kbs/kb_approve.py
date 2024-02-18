from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_approve() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да, вопрос решён")
    kb.button (text="Нет, уточнить вопрос")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)