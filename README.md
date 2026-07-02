# MixaUC Bot — @mixauc_bot

PUBG Mobile UC spin/referral/sotib olish/chiqarish boti.

## Bot imkoniyatlari

- 🎰 Har kuni 3 marta bepul spin (asosan 1-3 UC, kamdan-kam katta miqdorlar)
- 👥 Referal tizimi — har bir taklif qilingan do'st uchun +1 spin
- 🛒 UC sotib olish — Midasbuy narxlariga mos paketlar, tanlagach admin (@abe_vlog) bilan bog'lanish tugmasi chiqadi va adminga xabar yuboriladi
- 💸 UC chiqarish — balans kamida 60 UC bo'lsa, 60 yoki 120 UC tanlab, o'yin ID kiritib so'rov yuborish mumkin. So'rov to'g'ridan-to'g'ri sizga (adminga) keladi

## Fayl tuzilishi

```
mixauc_bot/
  bot.py            — botni ishga tushiruvchi asosiy fayl
  config.py         — token, admin ID, narxlar, spin jadvali
  database.py       — SQLite (aiosqlite) bilan ishlash
  keyboards.py       — tugmalar
  states.py          — FSM holatlari (chiqarish uchun o'yin ID kutish)
  handlers/
    start.py         — /start, referal, balans
    spin.py           — spin logikasi
    buy.py            — UC sotib olish
    withdraw.py        — UC chiqarish
  requirements.txt
```

## O'zgartirish kerak bo'lgan joylar

`config.py` faylida:
- `SPIN_TABLE` — spin ehtimolliklarini xohlaganingizcha o'zgartirishingiz mumkin
- `UC_PACKAGES` — sotiladigan paketlar va narxlar (hozir Midasbuy AQSH narxlariga mos, o'z mintaqangiz narxiga moslashtiring)
- `MIN_WITHDRAW`, `WITHDRAW_OPTIONS` — chiqarish shartlari

## Botni lokal ishga tushirish

```bash
pip install -r requirements.txt
python bot.py
```

Bot polling rejimida ishlaydi (webhook shart emas), shuning uchun kompyuteringiz yoki serveringiz ishlab turgan payt bot javob beradi.

## Bepul hostingga deploy qilish (Railway misolida)

Railway sizning oldingi loyihalaringiz (masalan, Usta Top) uchun ham ishlatilgan, shu sababli eng qulay variant:

1. GitHub'da yangi repo yarating va shu papkadagi barcha fayllarni yuklang (`.env` faylini hech qachon repo'ga qo'ymang, token config.py ichida bo'lsa ham xavfsizlik uchun uni Railway'ning Environment Variables bo'limiga ko'chirib, `config.py`da `os.getenv("BOT_TOKEN")` orqali o'qishni tavsiya qilaman).
2. [railway.app](https://railway.app) da "New Project" → "Deploy from GitHub repo" tanlang, repo'ni ulang.
3. Start Command: `python bot.py`
4. SQLite fayli (`database.db`) qayta deploy qilinganda o'chib ketmasligi uchun Railway'da **Volume** qo'shing va uni loyihaning ildiz papkasiga (yoki `DB_PATH` ko'rsatilgan joyga) ulang — aks holda har deploy'da foydalanuvchilar bazasi tozalanadi.
5. Deploy tugagach, loglarda "Update polling" ko'rinsa — bot ishga tushgan.

**Muhim:** Railway va shu kabi platformalarning bepul limitlari tez-tez o'zgarib turadi (oylik kredit, sleep rejimi va h.k.), shuning uchun deploy qilishdan oldin joriy shartlarni saytda tekshirib oling. Agar bot doimiy uzluksiz ishlashi kerak bo'lsa, eng ishonchli variant — arzon VPS (masalan, oyiga $3-5) yoki mavjud serveringizda `systemd`/`screen`/`pm2` orqali ishga tushirish.

### Oddiy VPS'da doimiy ishga tushirish (systemd misoli)

```ini
# /etc/systemd/system/mixauc_bot.service
[Unit]
Description=MixaUC Telegram Bot
After=network.target

[Service]
WorkingDirectory=/root/mixauc_bot
ExecStart=/usr/bin/python3 bot.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable mixauc_bot
sudo systemctl start mixauc_bot
```

## Eslatma

- Bot tokenini hech kimga oshkor qilmang — agar oshkor bo'lgan bo'lsa, @BotFather orqali `/revoke` qilib yangi token oling.
- `database.db` faylini muntazam zaxira (backup) qilib turing — foydalanuvchilar balansi shu yerda saqlanadi.
