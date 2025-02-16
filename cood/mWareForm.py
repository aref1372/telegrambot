# mWareForm.py
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, PhotoSize
from aiogram.filters.command import Command
import databasseRobat
from databasseRobat import db_manage
from aiogram import F

class ProductForm(StatesGroup):
    photo = State()
    name = State()
    price = State()
    description = State()
    packaging = State()

async def start_product_submission(message: Message, state: FSMContext):
    await message.answer("📷 لطفاً تصویر محصول را ارسال کنید:")
    await state.set_state(ProductForm.photo)

async def process_photo(message: Message, state: FSMContext):
    photo: PhotoSize = message.photo[-1]
    await state.update_data(photo=photo.file_id)
    await message.answer("📌 نام محصول را وارد کنید:")
    await state.set_state(ProductForm.name)

async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("💰 قیمت محصول را وارد کنید:")
    await state.set_state(ProductForm.price)

async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("📝 توضیحات محصول را وارد کنید:")
    await state.set_state(ProductForm.description)

async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("📦 نوع بسته‌بندی محصول را وارد کنید:")
    await state.set_state(ProductForm.packaging)

async def process_packaging(message: Message, state: FSMContext):
    product_data = await state.get_data()
    # تنظیم ترتیب پارامترها مطابق با متد add_product:
    db_manage.add_product(
        message.from_user.id, 
        product_data["name"], 
        product_data["price"], 
        product_data["description"], 
        product_data["packaging"], 
        product_data["photo"]
    )
    await message.answer("✅ محصول شما با موفقیت ذخیره شد!")
    await state.clear()

def register_product_handlers(dp: Dispatcher):
    dp.message.register(start_product_submission, Command("add_product"))
    dp.message.register(process_photo, F.state == ProductForm.photo)
    dp.message.register(process_name, F.state == ProductForm.name)
    dp.message.register(process_price, F.state == ProductForm.price)
    dp.message.register(process_description, F.state == ProductForm.description)
    dp.message.register(process_packaging, F.state == ProductForm.packaging)