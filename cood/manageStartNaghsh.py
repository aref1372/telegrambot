
"""import asyncio
import logging
from aiogram import Dispatcher , Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import databasseRobat
from databasseRobat import db_manage
from keybord import role_selection_keyboard
import mAnmeldungFormBazaryab
import bot 

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    db_manage.add_user(user_id, username, full_name)  # ذخیره کاربر در دیتابیس

    await message.answer(f"سلام {full_name}! خوش آمدید.\n\n آیا مایلید به عنوان بازاریاب ثبت‌نام کنید؟", 
                     reply_markup=role_selection_keyboard)

async def role_selection(callback: CallbackQuery):
    if callback.data == "register_marketer":
        await callback.message.answer("لطفاً اطلاعات خود را برای ثبت‌نام وارد کنید.")
        state = callback.message.bot.dispatcher.current_state(user=callback.from_user.id)
        from mAnmeldungFormBazaryab import MarketerRegistrationHandler
        marketer_handler = MarketerRegistrationHandler(dp)
        await marketer_handler.start_marketer_registration(callback.message, state)
        #await (callback.message)
    elif callback.data == "not_interested":
        await callback.message.answer("ممنون! در صورت نیاز می‌توانید دوباره اقدام کنید.")

def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))
    dp.callback_query.register(role_selection, lambda c: c.data in ["register_marketer", "not_interested"])

    # ثبت هندلرهای ثبت‌نام FSM
def register_marketer_fsm_handlers(dp: Dispatcher):
    # این تابع را از کلاس MarketerRegistrationHandler فراخوانی می‌کنیم
    from mAnmeldungFormBazaryab import MarketerRegistrationHandler
    marketer_handler = MarketerRegistrationHandler(dp)
    marketer_handler.rigisterHandeler()

    


async def main():
    # تابع اصلی برای اجرای ربات 
    
    db = databasseRobat.DatabaseManager()
    db.connect_db()
    db.create_tables()  #یجاد جدول دیتابیس  
    

    register_start_handlers(dp)
    #register_marketer_handlers(dp)
    #register_product_handlers(dp)
    register_marketer_fsm_handlers(dp)"""
    

                