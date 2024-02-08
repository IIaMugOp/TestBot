from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from kbs.kb_wait import get_kb_wait
from kbs.kb_intro import get_kb_user
from kbs.kb_cancel import get_kb_cancel

router = Router()

message_link = {}

class Questions(StatesGroup):
    intro = State()
    question = State()


questions_count = {}

current_user_questions = {}




@router.message(Command(commands=["start"]))
async def cmd_start_user(message: Message):
    await message.answer(
        "Здравствуйте! Это бот технической поддержки.",
        reply_markup=get_kb_user()
    )




@router.message(Command(commands=["info"]))
async def cmd_start(message: Message):
    await message.answer(
        "В этом боте вы можете задать вопрос технической поддержке",
        reply_markup=get_kb_user()
    )




@router.message(F.text.lower() == 'задать вопрос')
async def cmd_ask(message: Message, state: FSMContext):
    if questions_count.get(message.from_user.id) == 1:
        await message.answer(
            text='Вы уже задали вопрос.',
            reply_markup=get_kb_user()
        )
    else:
        await message.answer(
            text="Задавайте Ваш вопрос:",
            reply_markup=get_kb_cancel()
        )
        await state.set_state(Questions.question)
        # Устанавливаем пользователю состояние "задаёт вопрос"



@router.message(F.text.lower() == 'статус вопроса')
async def cmd_check(message: Message, state: FSMContext):
    if questions_count.get(message.from_user.id):
        await message.answer(
            text='Вы задали вопрос, ожидайте',
            reply_markup=get_kb_wait()
        )
    else:
        await message.answer(
            text="Нет текущего вопроса. Хотите задать вопрос службе поддержки?",
            reply_markup=get_kb_user()
        )