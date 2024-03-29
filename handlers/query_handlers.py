from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from kbs.kb_wait import get_kb_wait
from kbs.kb_intro import get_kb_user

from config import groupID
import psycopg2
from database_dir import db_storage

from .personal_command import Questions, current_user_questions, questions_count, message_link, answer_count
import datetime

router = Router()




@router.message(F.text.lower() == "отменить вопрос", db_storage.FilterNotQuestion())
async def cmd_cancel(message: Message):
    user_id = message.from_user.id
    # Найти message_id сообщения в группе, соответствующего пользователю
    message_id_to_delete = None
    for original_user_id, group_message_id in message_link.items():
        if original_user_id == user_id:
            message_id_to_delete = group_message_id
            break

    if message_id_to_delete and not answer_count.get(message_id_to_delete):
        try:
            # Попытка удалить сообщение в группе
            print(f"Попытка удалить сообщение с ID: {message_id_to_delete}")
            await message.bot.delete_message(chat_id=groupID, message_id=message_id_to_delete)
            print("Сообщение успешно удалено")
            current_user_questions[user_id] = None
            questions_count[original_user_id] = 0

        except Exception as e:
            # Обработка возможных исключений, например, если сообщение уже удалено
            print(f"Ошибка при удалении сообщения: {e}")
    else:
        current_user_questions[user_id] = None
        questions_count[original_user_id] = 0

    await message.answer(
        text=f"У вас нет активных вопросов, хотите задать новый?",
        reply_markup=get_kb_user()
    )





@router.message(F.text.lower() == 'посмотреть текущий вопрос')
async def cmd_start(message: Message):
    if not questions_count.get(message.from_user.id):
        await message.answer(
            "Текущего вопроса нет. Хотите задать вопрос службе поддержки?",
            reply_markup=get_kb_user()
        )
    else:
        await message.answer(
            text=f"Ваш текущий вопрос: {current_user_questions[message.from_user.id]}",
            reply_markup=get_kb_wait()
        )




@router.message(F.text.lower() == 'главное меню')
async def cmd_start(message: Message):
    if not questions_count.get(message.from_user.id):
        await message.answer(
            "Текущего вопроса нет. Хотите задать вопрос службе поддержки?",
            reply_markup=get_kb_user()
        )
    else:
        await message.answer(
            text=f"Ваш текущий вопрос: {current_user_questions[message.from_user.id]}",
            reply_markup=get_kb_user()
        )





@router.message(F.text.lower() == 'отмена', db_storage.FilterQuestion())
async def cancel(message: Message, state: FSMContext):
    await message.answer(
        "Хотите задать вопрос службе поддержки?",
        reply_markup=get_kb_user()
    )
    with db_storage.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO question_table (cancel)  VALUES (%s) ",
                (1))
            db_storage.conn.commit()



@router.message(F.text | F.photo, db_storage.FilterQuestion())
async def forward_to_group(message: Message):
    questions_count[message.from_user.id] = 0
    await message.answer(
        "Ваш вопрос отправлен. Ожидайте",
        reply_markup=get_kb_user()
    )

    forwarded_message = await message.forward(chat_id=groupID)
    message_link[message.from_user.id] = forwarded_message.message_id
    questions_count[message.from_user.id] = 1
    current_user_questions[message.from_user.id] = message.text

    answer_count[message.message_id] = 0
    db_storage.set_state_db(message.from_user.id, 0)

    with db_storage.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO question_table (user_id, message_id, question, answer, time)  VALUES (%s, %s, %s, %s, %s) ",
                (message.from_user.id, message.message_id, message.text, 0, datetime.datetime.now()))
            db_storage.conn.commit()



@router.message(F.text)
async def any_message(message: Message):
    if not questions_count.get(message.from_user.id):
        await message.answer(
            "Хотите задать вопрос службе поддержки?",
            reply_markup=get_kb_user()
        )
    else:
        await message.answer(
            "У вас есть активный вопрос",
            reply_markup=get_kb_user()
        )