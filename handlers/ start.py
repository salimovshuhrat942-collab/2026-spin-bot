# handlers/start.py

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message

import database as db
from config import REFERRAL_BONUS_SPINS
from keyboards import main_menu_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    existing = await db.get_user(user_id)
    referred_by = None

    if command.args and command.args.startswith("ref_"):
        try:
            ref_id = int(command.args.replace("ref_", ""))
            if ref_id != user_id:
                referred_by = ref_id
        except ValueError:
            pass

    if not existing:
        await db.create_user(user_id, username, referred_by)

        # Agar referal orqali kelgan bo'lsa — taklif qilgan odamga bonus spin beramiz
        if referred_by:
            referrer = await db.get_user(referred_by)
            if referrer:
                await db.add_spin(referred_by, REFERRAL_BONUS_SPINS)
                await db.increment_referral(referred_by)
                try:
                    await bot.send_message(
                        referred_by,
                        f"🎉 Sizning taklifingiz bilan yangi do'stingiz botga qo'shildi!\n"
                        f"Sizga +{REFERRAL_BONUS_SPINS} bonus spin berildi 🎰"
                    )
                except Exception:
                    pass

    await db.ensure_daily_reset(user_id)

    await message.answer(
        "👋 Xush kelibsiz, <b>MixaUC</b> botiga!\n\n"
        "🎰 Har kuni <b>3 marta bepul</b> spin qilib UC yutib olishingiz mumkin.\n"
        "👥 Har bir taklif qilgan do'stingiz uchun <b>+1 qo'shimcha spin</b> olasiz.\n"
        "🛒 UC sotib olishni ham xohlasangiz — pastdagi menyudan foydalaning.\n\n"
        "Quyidagi menyudan birini tanlang 👇",
        reply_markup=main_menu_kb()
    )


@router.message(F.text == "💰 Balansim")
async def show_balance(message: Message):
    user_id = message.from_user.id
    await db.ensure_daily_reset(user_id)
    user = await db.get_user(user_id)
    if not user:
        await db.create_user(user_id, message.from_user.username or message.from_user.full_name)
        user = await db.get_user(user_id)

    await message.answer(
        f"💰 Balansingiz: <b>{user['uc_balance']} UC</b>\n"
        f"🎰 Qolgan spinlar: <b>{user['spins_left']}</b>\n"
        f"👥 Taklif qilingan do'stlar: <b>{user['ref_count']}</b>"
    )


@router.message(F.text == "👥 Do'st taklif qilish")
async def referral_link(message: Message, bot: Bot):
    bot_info = await bot.get_me()
    link = f"https://t.me/{bot_info.username}?start=ref_{message.from_user.id}"
    await message.answer(
        "👥 Do'stingizni taklif qiling va har bir do'st uchun <b>+1 bepul spin</b> oling!\n\n"
        f"🔗 Sizning havolangiz:\n{link}"
    )
