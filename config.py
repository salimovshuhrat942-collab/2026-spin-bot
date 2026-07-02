# config.py
# Bot sozlamalari

BOT_TOKEN = "7046650654:AAGmddTLzLfbFxYMlR2PVguEUdyy3qm5cek"

ADMIN_ID = 8007670371            # Adminning telegram ID raqami
ADMIN_USERNAME = "abe_vlog"       # Adminning telegram useri (@ belgisisiz)

DB_PATH = "database.db"

# Har kuni nechta bepul spin beriladi
DAILY_SPINS = 3

# Har bir do'st taklif qilinganda beriladigan qo'shimcha spin soni
REFERRAL_BONUS_SPINS = 1

# UC chiqarish (withdraw) sozlamalari
MIN_WITHDRAW = 60                 # eng kam chiqarish miqdori
WITHDRAW_OPTIONS = [60, 120]      # foydalanuvchi tanlaydigan miqdorlar

# Spin natijalarining ehtimollik jadvali: (UC miqdori, og'irlik)
# Og'irlik qancha katta bo'lsa, shuncha ko'p tushadi.
# 1-3 UC eng ko'p tushadi (~85%), qolganlari juda kam (~15%) tushadi.
SPIN_TABLE = [
    (1, 350),
    (2, 300),
    (3, 200),
    (5, 80),
    (10, 40),
    (20, 15),
    (50, 8),
    (100, 4),
    (300, 2),
    (1000, 1),
]

# Sotib olish uchun UC paketlari (Midasbuy (USA) rasmiy narxlariga mos, taxminiy)
# Foydalanuvchi buni bossa -> admin bilan bog'lanish tugmasi chiqadi
UC_PACKAGES = [
    (60, "$0.99"),
    (325, "$4.99"),
    (660, "$9.99"),
    (1800, "$24.99"),
    (3850, "$49.99"),
    (8100, "$99.99"),
]
