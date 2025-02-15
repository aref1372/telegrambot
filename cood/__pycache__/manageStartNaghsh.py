# handlers/start_handler.py (مدیریت استارت و انتخاب نقش)
from aiogram import Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from databasseRobat import db_manage
import databasseRobat
from keybord import role_selection_keyboard
from mAnmeldungFormBazaryab import start_marketer_registration

async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    databasseRobat.add_user(user_id, username, full_name)  # ذخیره کاربر در دیتابیس

    await message.answer(f"سلام {full_name}! خوش آمدید.\n\n آیا مایلید به عنوان بازاریاب ثبت‌نام کنید؟", 
                         reply_markup=role_selection_keyboard())

async def role_selection(callback: CallbackQuery):
    if callback.data == "register_marketer":
        await callback.message.answer("لطفاً اطلاعات خود را برای ثبت‌نام وارد کنید.")
        from mAnmeldungFormBazaryab import start_marketer_registration
        await start_marketer_registration(callback.message)
    elif callback.data == "not_interested":
        await callback.message.answer("ممنون! در صورت نیاز می‌توانید دوباره اقدام کنید.")

def register_start_handlers(dp: Dispatcher):
    dp.message.register(start_handler, Command("start"))
    dp.callback_query.register(role_selection, lambda c: c.data in ["register_marketer", "not_interested"])