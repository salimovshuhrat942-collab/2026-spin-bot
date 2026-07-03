# handlers/spin.py

import random

from aiogram import Router, F
from aiogram.types import Message

import database as db
from config import SPIN_TABLE

router = Router()


def roll_spin() -> int:
    amounts = [a for a, w in SPIN_TABLE]
    weights = [w for a, w in SPIN_TABLE]
    return random.choices(amounts, weights=weights, k=1)[0]


@router.message(F.text == "🎰 Spin qilish")
async def do_spin(message: Message):
    user_id = message.from_user.id
    await db.ensure_daily_reset(user_id)

    user = await db.get_user(user_id)
    if not user:
        await db.create_user(user_id, message.from_user.username or message.from_user.full_name)
        user = await db.get_user(user_id)

    if user["spins_left"] <= 0:
        await message.answer(
            "😔 Bugungi bepul spinlaringiz tugadi.\n\n"
            "🕛 Ertaga qayta urinib ko'ring yoki 👥 do'stlaringizni taklif qilib "
            "qo'shimcha spin oling!"
        )
        return

    won = roll_spin()
    await db.decrement_spin(user_id)
    await db.add_balance(user_id, won)

    updated = await db.get_user(user_id)

    if won >= 20:
        prefix = "🎉🎉 KATTA YUTUQ! 🎉🎉"
    else:
        prefix = "🎰 Natija:"

    await message.answer(
        f"{prefix}\n\n"
        f"Siz <b>{won} UC</b> yutdingiz!\n\n"
        f"💰 Yangi balans: <b>{updated['uc_balance']} UC</b>\n"
        f"🎰 Qolgan spinlar: <b>{updated['spins_left']}</b>"
    )
