# keyboards.py

from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)

from config import UC_PACKAGES, WITHDRAW_OPTIONS, ADMIN_USERNAME


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎰 Spin qilish"), KeyboardButton(text="💰 Balansim")],
            [KeyboardButton(text="👥 Do'st taklif qilish"), KeyboardButton(text="🛒 UC sotib olish")],
            [KeyboardButton(text="💸 UC chiqarish")],
        ],
        resize_keyboard=True
    )
    return kb


def buy_uc_kb() -> InlineKeyboardMarkup:
    rows = []
    for amount, price in UC_PACKAGES:
        rows.append([InlineKeyboardButton(
            text=f"{amount} UC — {price}",
            callback_data=f"buy_{amount}_{price}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def contact_admin_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Admin bilan bog'lanish", url=f"https://t.me/{ADMIN_USERNAME}")]
    ])


def withdraw_options_kb(balance: int) -> InlineKeyboardMarkup:
    rows = []
    for amount in WITHDRAW_OPTIONS:
        if balance >= amount:
            rows.append([InlineKeyboardButton(text=f"{amount} UC chiqarish", callback_data=f"wd_{amount}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
