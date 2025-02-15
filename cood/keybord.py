"""from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

role_selection_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎭 ثبت‌نام به عنوان بازاریاب")],
        [KeyboardButton(text="🏭 ثبت‌نام به عنوان تأمین‌کننده")],
    ],
    resize_keyboard=True 
) """

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# تعریف دکمه‌ها با استفاده از مقداردهی به صورت استاندارد
register_button = InlineKeyboardButton(text="ثبت‌نام به عنوان بازاریاب", callback_data="register_marketer")
not_interested_button = InlineKeyboardButton(text="مشتاق نیستم", callback_data="not_interested")

# ایجاد کیبورد و اضافه کردن دکمه‌ها
role_selection_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [register_button],  # دکمه اول
    [not_interested_button]  # دکمه دوم
])