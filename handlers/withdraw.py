# handlers/withdraw.py

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.types import ReplyKeyboardRemove

import database as db
from config import ADMIN_ID, MIN_WITHDRAW
from keyboards import withdraw_options_kb, main_menu_kb
from states import WithdrawStates

router = Router()


@router.message(F.text == "💸 UC chiqarish")
async def start_withdraw(message: Message):
    user_id = message.from_user.id
    await db.ensure_daily_reset(user_id)
    user = await db.get_user(user_id)
    if not user:
        await db.create_user(user_id, message.from_user.username or message.from_user.full_name)
        user = await db.get_user(user_id)

    if user["uc_balance"] < MIN_WITHDRAW:
        await message.answer(
            f"❗️ UC chiqarish uchun kamida <b>{MIN_WITHDRAW} UC</b> yig'ishingiz kerak.\n\n"
            f"💰 Hozirgi balansingiz: <b>{user['uc_balance']} UC</b>\n"
            "🎰 Spin qilishda davom eting!"
        )
        return

    await message.answer(
        f"💸 Balansingiz: <b>{user['uc_balance']} UC</b>\n\n"
        "Qancha UC chiqarmoqchisiz?",
        reply_markup=withdraw_options_kb(user["uc_balance"])
    )


@router.callback_query(F.data.startswith("wd_"))
async def choose_withdraw_amount(callback: CallbackQuery, state: FSMContext):
    amount = int(callback.data.split("_")[1])
    user = await db.get_user(callback.from_user.id)

    if not user or user["uc_balance"] < amount:
        await callback.answer("Balansingiz yetarli emas.", show_alert=True)
        return

    await state.update_data(withdraw_amount=amount)
    await state.set_state(WithdrawStates.waiting_game_id)

    await callback.message.answer(
        f"🆔 <b>{amount} UC</b> chiqarish uchun PUBG Mobile o'yin ID raqamingizni yuboring:",
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.answer()


@router.message(WithdrawStates.waiting_game_id)
async def receive_game_id(message: Message, state: FSMContext, bot: Bot):
    game_id = message.text.strip()

    if not game_id.isdigit():
        await message.answer("❗️ Iltimos, faqat raqamlardan iborat to'g'ri o'yin ID yuboring:")
        return

    data = await state.get_data()
    amount = data.get("withdraw_amount")
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    success = await db.deduct_balance(user_id, amount)
    if not success:
        await message.answer("❗️ Balansingiz yetarli emas. Amal bekor qilindi.", reply_markup=main_menu_kb())
        await state.clear()
        return

    withdrawal_id = await db.create_withdrawal(user_id, username, amount, game_id)

    await message.answer(
        f"✅ So'rovingiz qabul qilindi!\n\n"
        f"📦 Miqdor: <b>{amount} UC</b>\n"
        f"🆔 O'yin ID: <code>{game_id}</code>\n\n"
        "Tez orada UC hisobingizga o'tkaziladi. Rahmat! 🙌",
        reply_markup=main_menu_kb()
    )

    try:
        await bot.send_message(
            ADMIN_ID,
            "💸 <b>Yangi UC chiqarish so'rovi!</b>\n\n"
            f"🔖 So'rov ID: <code>{withdrawal_id}</code>\n"
            f"👤 Foydalanuvchi: @{username} (ID: <code>{user_id}</code>)\n"
            f"📦 Miqdor: <b>{amount} UC</b>\n"
            f"🆔 O'yin ID: <code>{game_id}</code>"
        )
    except Exception:
        pass

    await state.clear()
