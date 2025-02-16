# mAnmeldungFormBazaryab.py
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Dispatcher
import databasseRobat
from databasseRobat import db_manage
from aiogram import F

class MarketerForm(StatesGroup):
    location = State()
    national_id = State()
    phone_number = State()

class MarketerRegistrationHandler:
    def __init__(self, dp: Dispatcher):
        self.dp = dp

    async def start_marketer_registration(self, message: Message, state: FSMContext):   
        await message.answer("📍 لطفاً محل سکونت خود را وارد کنید:")
        await state.set_state(MarketerForm.location)
         # چاپ مقدار وضعیت برای بررسی
        current_state = await state.get_state()
        print("Current FSM state:", current_state)

    async def process_location(self, message: Message, state: FSMContext):
        await state.update_data(location=message.text)
        await message.answer("🆔 لطفاً شماره ملی خود را وارد کنید:")
        await state.set_state(MarketerForm.national_id)

    async def process_national_id(self, message: Message, state: FSMContext):
        await state.update_data(national_id=message.text)
        await message.answer("📞 لطفاً شماره تماس خود را وارد کنید:")
        await state.set_state(MarketerForm.phone_number)

    async def process_phone_number(self, message: Message, state: FSMContext):
        user_data = await state.get_data()
        db_manage.add_marketer(
            message.from_user.id, 
            message.from_user.username, 
            message.from_user.full_name, 
            user_data["national_id"], 
            message.text, 
            user_data["location"]
        )
        await message.answer("✅ شما با موفقیت به عنوان بازاریاب ثبت شدید!")
        await state.clear()

    def register_handlers(self):
        self.dp.message.register(self.start_marketer_registration, Command("register_marketer"))
        # استفاده از فیلتر F.state برای فیلتر کردن پیام‌ها بر اساس وضعیت
        #self.dp.message.register(self.process_location, F.state == MarketerForm.location.state)
        #self.dp.message.register(self.process_national_id, F.state == MarketerForm.national_id.state)
        #self.dp.message.register(self.process_phone_number, F.state == MarketerForm.phone_number.state)
        # گزینه 2 (در صورت نیاز): استفاده از مقادیر رشته‌ای
        self.dp.message.register(self.process_location, F.state == "MarketerForm:location")
        self.dp.message.register(self.process_national_id, F.state == "MarketerForm:national_id")
        self.dp.message.register(self.process_phone_number, F.state == "MarketerForm:phone_number")