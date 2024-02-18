import psycopg2
from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import host, db_name, user, password



def set_state_db(user_id, user_status):
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO status_table (user_id, user_status) VALUES (%s, %s) "
                "ON CONFLICT (user_id) DO UPDATE SET user_status = EXCLUDED.user_status",
                (user_id, user_status))
            conn.commit()


def get_state_db(user_id):
    with conn.cursor() as cur:
        cur.execute("SELECT user_status FROM status_table WHERE user_id = %s", (user_id,))
        result = cur.fetchone()
        return result[0] if result else None



class FilterQuestion(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return get_state_db(message.from_user.id) == 1


class FilterNotQuestion(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return get_state_db(message.from_user.id) != 1




try:
    conn = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    print("Подключение к базе данных успешно")
    cursor = conn.cursor()
except psycopg2.Error as e:
    print(f"Ошибка при подключении к базе данных: {e}")
