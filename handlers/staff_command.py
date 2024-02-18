from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from kbs.kb_staff import get_kb_staff
from kbs.kb_approve import get_kb_approve

from config import groupID
import psycopg2
from database_dir import db_storage

from .personal_command import message_link, questions_count, current_user_questions, answer_count
from help_functions import find_user_by_message_id


router = Router()


@router.message(F.chat.id == groupID, Command(commands=["start"]))
async def cmd_start_staff(message: Message):
    await message.answer(
        text='Меню для технической поддержки',
        reply_markup=get_kb_staff()
    )


@router.message(F.chat.id == groupID, F.text == 'Текущий вопрос')
async def current_question(message: Message):
    #await message.bot.send_message(chat_id=groupID, text=f'Данная функция находится в разработке')
    with db_storage.conn.cursor() as cur:
        cur.execute(
            """SELECT user_id, question
            FROM question_table
            WHERE answer = 0
            ORDER BY time ASC
            LIMIT 1"""
        )
        db_storage.conn.commit()
        result = cur.fetchone()
        if result:
            user_id, question = result
            await message.bot.send_message(chat_id=groupID, text=question)
        else:
            await message.bot.send_message(chat_id=groupID, text='Вопросы, на которые не ответила техническая поддержка - отсутствуют')




@router.message(F.chat.id == groupID, F.text.lower() == 'количество текущих вопросов')
async def get_count_current_questions(message: Message):
    if current_user_questions:
      await message.bot.send_message(chat_id=groupID, text=f'Количество активных вопросов - {sum(1 for value in current_user_questions.values() if value is not None)}')
    else:
        await message.bot.send_message(chat_id=groupID, text='Вопросы, на которые не ответила техническая поддержка - отсутствуют')


@router.message(F.chat.id == groupID)
async def group_reply(message: Message):
       # Проверка, является ли сообщение ответом на пересланное сообщение
       if message.reply_to_message:
           original_user_id = find_user_by_message_id(message.reply_to_message.message_id, message_link)
           # Отправка сообщения от имени бота оригинальному отправителю
           await message.bot.send_message(
               original_user_id,
               message.text,reply_markup=get_kb_approve()
            )

           # Количество ответов на заданный вопрос
           if questions_count[original_user_id]:
              questions_count[original_user_id] = 0
           current_user_questions[message.from_user.id] = None
           answer_count.setdefault(message.reply_to_message.message_id, 0)
           answer_count[message.reply_to_message.message_id] += 1
