# mStartNaghsh.py
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import databasseRobat
from databasseRobat import db_manage
from keybord import role_selection_keyboard
import mAnmeldungFormBazaryab
import mWareForm
from mWareForm import register_product_handlers
from aiogram.fsm.storage.memory import MemoryStorage
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def catch_all(message: Message):
    print("Catch-all received message:", message.text)

dp.message.register(catch_all)


# توکن ربات (توکن واقعی خود را جایگزین کنید)
TOKEN = "8161913266:AAG6Ls1vcNtXEk53p9vrMTDAaP93UNn0Dsg"

# ایجاد نمونه‌های Bot و Dispatcher
bot = Bot(token=TOKEN)


async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    db_manage.add_user(user_id, username, full_name)
    await message.answer(
        f"سلام {full_name}! خوش آمدید.\n\nآیا مایلید به عنوان بازاریاب ثبت‌ نام کنید؟",
        reply_markup=role_selection_keyboard
    )

async def role_selection(callback: CallbackQuery):
    await callback.answer()  # پاسخ به callback تا loader پاک شود

    if callback.data == "register_marketer":
        await callback.message.answer("لطفاً اطلاعات خود را برای ثبت‌نام وارد کنید.")
        # استفاده از FSMContext به صورت positional
        from aiogram.fsm.context import FSMContext
        state = FSMContext(dp.storage, (callback.message.chat.id, callback.from_user.id))
        from mAnmeldungFormBazaryab import MarketerRegistrationHandler
        marketer_handler = MarketerRegistrationHandler(dp)
        await marketer_handler.start_marketer_registration(callback.message, state)
    elif callback.data == "not_interested":
        await callback.message.answer("ممنون! در صورت نیاز می‌توانید دوباره اقدام کنید.")

def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))
    dp.callback_query.register(role_selection, lambda c: c.data in ["register_marketer", "not_interested"])

def register_marketer_fsm_handlers(dp: Dispatcher):
    from mAnmeldungFormBazaryab import MarketerRegistrationHandler
    marketer_handler = MarketerRegistrationHandler(dp)
    marketer_handler.register_handlers()

async def main():
    # تنظیمات دیتابیس
    db = databasseRobat.DatabaseManager()
    db.connect_db()
    db.create_tables()

    # ثبت هندلرهای عمومی و FSM
    register_start_handlers(dp)
    register_marketer_fsm_handlers(dp)
    register_product_handlers(dp)  # از mWareForm
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    