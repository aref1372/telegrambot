from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

role_selection_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎭 ثبت‌نام به عنوان بازاریاب")],
        [KeyboardButton(text="🏭 ثبت‌نام به عنوان تأمین‌کننده")],
    ],
    resize_keyboard=True
)