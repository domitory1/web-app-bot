from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

application_number_phone = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
   [KeyboardButton(text="Поделиться номером", request_contact=True)],
])

inline_menu = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
   [InlineKeyboardButton(text="Меню", web_app=WebAppInfo(url='https://webappmenu-meridian.netlify.app'))],
   [InlineKeyboardButton(text="Корзина", web_app=WebAppInfo(url='https://webappmenu-meridian.netlify.app'))],
])

markup_admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
   [KeyboardButton(text='Редактировать приветственные сообщения', callback_data = '/edit_welcome_message')],
   [KeyboardButton(text='Редактировать меню (бот)', callback_data = '/edit_menu_bot')],
   [KeyboardButton(text='Редактировать меню (сайт)', callback_data = '/edit_menu_site')],
])
