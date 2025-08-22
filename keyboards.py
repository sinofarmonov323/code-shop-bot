from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def menu_uz():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💸 Kod sotish", callback_data="sell_code"), InlineKeyboardButton(text="👤 Profil", callback_data="profile")]
        ]
    )

def menu_ru():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💸 Продажа кода", callback_data="sell_code")],
            [InlineKeyboardButton(text="📝 Посмотреть мои коды", callback_data="my_codes")],
        ]
    )

def skip():
    return ReplyKeyboardMarkup(
        resize_keyboard=True, keyboard=[
            [KeyboardButton(text="🛑 tashlab ketish")]
        ]
    )

def yes_or_no():
    return ReplyKeyboardMarkup(
        resize_keyboard=True, keyboard=[
            [KeyboardButton(text="✅ Ha"), KeyboardButton(text="❌ Yo'q")]
        ]
    )

def choose_language():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="uz"), InlineKeyboardButton(text="🇷🇺 Русский", callback_data='ru')]
        ]
    )

def see_codes():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Kodlarni ko'rish", callback_data="see_codes")]
        ]
    )
