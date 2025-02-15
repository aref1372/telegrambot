#  handlers/marketer_form.py (مدیریت فرم ثبت‌نام بازاریاب)


from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import databasseRobat

class MarketerForm(StatesGroup):
    location = State()
    national_id = State()
    phone_number = State()

async def start_marketer_registration(message: Message, state: FSMContext):
    await message.answer("📍 لطفاً محل سکونت خود را وارد کنید:")
    await state.set_state(MarketerForm.location)

async def process_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await message.answer("🆔 لطفاً شماره ملی خود را وارد کنید:")
    await state.set_state(MarketerForm.national_id)

async def process_national_id(message: Message, state: FSMContext):
    await state.update_data(national_id=message.text)
    await message.answer("📞 لطفاً شماره تماس خود را وارد کنید:")
    await state.set_state(MarketerForm.phone_number)

async def process_phone_number(message: Message, state: FSMContext):
    user_data = await state.get_data()
    databasseRobat.add_marketer(
        message.from_user.id, user_data["location"], user_data["national_id"], message.text
    )
    await message.answer("✅ شما با موفقیت به عنوان بازاریاب ثبت شدید!")
    await state.clear()

def register_marketer_handlers(dp: Dispatcher):
    dp.message.register(start_marketer_registration, commands=["register_marketer"])
    dp.message.register(process_location, MarketerForm.location)
    dp.message.register(process_national_id, MarketerForm.national_id)
    dp.message.register(process_phone_number, MarketerForm.phone_number)