import asyncpg
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from handlers.users.currency_rate import rate_eur, rate_usd
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        user = await db.add_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name,
                                 username=message.from_user.username)
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    count = await db.count_users()

    # Забираем как список или как словарь
    user_data = list(user)
    user_data_dict = dict(user)

    # Забираем напрямую как из списка или словаря
    username = user.get("username")
    full_name = user[2]

    await message.answer(
        "\n".join(
            [
                f'Привет, {message.from_user.full_name}!',
                f'\nТекущий курс ЦБ РФ: '
                f'\n<strong>{rate_usd.name}</strong>: {rate_usd.rate}',
                f'<strong>{rate_eur.name}</strong>: {rate_eur.rate}'
            ]), parse_mode=types.ParseMode.HTML)
