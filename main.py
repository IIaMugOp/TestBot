import asyncio
from aiogram import Bot, Dispatcher
from handlers import personal_command, query_handlers, staff_command
from config import botToken


# Запуск бота
async def main():
    bot = Bot(token=botToken)
    dp = Dispatcher()

    #регистрация роутеров по одному на строку
    dp.include_router(staff_command.router)
    dp.include_router(personal_command.router)
    dp.include_router(query_handlers.router)

    # Запускаем бота и пропускаем все накопленные входящие
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())