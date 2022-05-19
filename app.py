import logging

import middlewares, filters, handlers  # noqa

from aiogram import executor, Dispatcher

from loader import dp, db
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher: Dispatcher):
    # Уведомляет про запуск
    logging.info("Создаем подключение к базе данных")


    logging.info("Создаем таблицу пользователей")
    await db.create_table_users()
    logging.info("Готово.")

    await on_startup_notify(dispatcher)


async def on_shutdown(_: Dispatcher):
    await db.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
