import databasseRobat
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import F
from aiogram.filters.command import Command





# توکن ربات که از BotFather دریافت کردید
TOKEN = "8161913266:AAG6Ls1vcNtXEk53p9vrMTDAaP93UNn0Dsg"

# راه‌اندازی لاگ‌ها
logging.basicConfig(level=logging.INFO)

# ایجاد شیء Bot و Dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# پیام خوش‌آمدگویی
@dp.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    databasseRobat.add_user(user_id, username, full_name)  # ذخیره کاربر در دیتابیس

    await message.answer(f" Hello {full_name}! herrzlichwelcemmen in Robat ")

async def on_start():
    databasseRobat.create_table()
                                
    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped")
        await bot.close()

if __name__ == "__main__":
    asyncio.run(on_start())