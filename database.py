# database.py
# SQLite orqali foydalanuvchilar va chiqarish so'rovlarini saqlash

import aiosqlite
from datetime import datetime, timezone, timedelta

from config import DB_PATH, DAILY_SPINS

# Toshkent vaqti (UTC+5) — kunlik spin reset shu vaqt bo'yicha hisoblanadi
TASHKENT_TZ = timezone(timedelta(hours=5))


def today_str() -> str:
    return datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                uc_balance INTEGER DEFAULT 0,
                spins_left INTEGER DEFAULT 3,
                last_reset TEXT,
                referred_by INTEGER,
                ref_count INTEGER DEFAULT 0,
                joined_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS withdrawals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                amount INTEGER,
                game_id TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            )
        """)
        await db.commit()


async def get_user(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = await cur.fetchone()
        return dict(row) if row else None


async def create_user(user_id: int, username: str, referred_by: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR IGNORE INTO users
               (user_id, username, uc_balance, spins_left, last_reset, referred_by, ref_count, joined_at)
               VALUES (?, ?, 0, ?, ?, ?, 0, ?)""",
            (user_id, username, DAILY_SPINS, today_str(), referred_by,
             datetime.now(TASHKENT_TZ).isoformat())
        )
        await db.commit()


async def ensure_daily_reset(user_id: int):
    """Agar bugungi kun uchun spinlar hali reset qilinmagan bo'lsa, qayta to'ldiradi."""
    user = await get_user(user_id)
    if not user:
        return
    if user["last_reset"] != today_str():
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                "UPDATE users SET spins_left = ?, last_reset = ? WHERE user_id = ?",
                (DAILY_SPINS, today_str(), user_id)
            )
            await db.commit()


async def decrement_spin(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET spins_left = spins_left - 1 WHERE user_id = ? AND spins_left > 0",
            (user_id,)
        )
        await db.commit()


async def add_spin(user_id: int, count: int = 1):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET spins_left = spins_left + ? WHERE user_id = ?",
            (count, user_id)
        )
        await db.commit()


async def add_balance(user_id: int, amount: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET uc_balance = uc_balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()


async def deduct_balance(user_id: int, amount: int) -> bool:
    user = await get_user(user_id)
    if not user or user["uc_balance"] < amount:
        return False
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET uc_balance = uc_balance - ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()
    return True


async def increment_referral(referrer_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET ref_count = ref_count + 1 WHERE user_id = ?",
            (referrer_id,)
        )
        await db.commit()


async def create_withdrawal(user_id: int, username: str, amount: int, game_id: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """INSERT INTO withdrawals (user_id, username, amount, game_id, status, created_at)
               VALUES (?, ?, ?, ?, 'pending', ?)""",
            (user_id, username, amount, game_id, datetime.now(TASHKENT_TZ).isoformat())
        )
        await db.commit()
        return cur.lastrowid
