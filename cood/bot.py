import logging
import asyncio
from aiogram import Bot, Dispatcher
from manageStartNaghsh import register_start_handlers
from mAnmeldungFormBazaryab import register_marketer_handlers
from mWareForm import register_product_handlers
import databasseRobat
from databasseRobat import db_manage

# توکن ربات که از BotFather دریافت کردید
TOKEN = "8161913266:AAG6Ls1vcNtXEk53p9vrMTDAaP93UNn0Dsg"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    """ تابع اصلی برای اجرای ربات """
    databasseRobat.create_table()  # ایجاد جدول دیتابیس

    # ثبت هندلرها
    register_start_handlers(dp)
    register_marketer_handlers(dp)
    register_product_handlers(dp)

    try:
        await dp.start_polling(bot)
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped")
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())

