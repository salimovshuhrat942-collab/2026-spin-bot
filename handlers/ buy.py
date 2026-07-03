# handlers/buy.py

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

from config import ADMIN_ID
from keyboards import buy_uc_kb, contact_admin_kb

router = Router()


@router.message(F.text == "🛒 UC sotib olish")
async def show_packages(message: Message):
    await message.answer(
        "🛒 <b>UC sotib olish</b>\n\n"
        "Narxlar Midasbuy rasmiy narxlariga teng.\n"
        "Kerakli paketni tanlang, so'ng admin bilan bog'lanib to'lovni amalga oshirasiz 👇",
        reply_markup=buy_uc_kb()
    )


@router.callback_query(F.data.startswith("buy_"))
async def handle_buy_selection(callback: CallbackQuery, bot: Bot):
    _, amount, price = callback.data.split("_", 2)
    user = callback.from_user

    await callback.message.answer(
        f"✅ Siz <b>{amount} UC</b> ({price}) paketini tanladingiz.\n\n"
        "To'lovni amalga oshirish uchun quyidagi tugma orqali admin bilan bog'laning 👇",
        reply_markup=contact_admin_kb()
    )

    try:
        await bot.send_message(
            ADMIN_ID,
            "🛒 <b>Yangi buyurtma!</b>\n\n"
            f"👤 Foydalanuvchi: @{user.username if user.username else user.full_name} "
            f"(ID: <code>{user.id}</code>)\n"
            f"📦 Tanlangan paket: <b>{amount} UC</b> — {price}"
        )
    except Exception:
        pass

    await callback.answer()
