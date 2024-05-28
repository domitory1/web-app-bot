import asyncio
import logging
import sys
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import Buttons.buttons as buttons
import Requests.requests as requests

API_TOKEN = "6658531652:AAEn5TRw5p4yHulphWYttyNfr2bQecvDNvU"
dp = Dispatcher()
bot = Bot(API_TOKEN, parse_mode=ParseMode.HTML)

message_texts_start = ["Добрый день! 😊", "Перед тем, как вы сделаете ваш первый заказ, поделитесь, пожалуйста, своим номером телефона. 😌\n"
                     "Он нужен для того, чтобы мы смогли добавить блюда именно в вашу корзину"]

@dp.message(CommandStart())
async def start_command(message: Message):
   if requests.check_user_id_in_db(message.from_user.id):
      await message.answer("Выберите раздел", reply_markup=buttons.inline_menu)
   else:
      for text in message_texts_start:
         if text != message_texts_start[-1]:
            await message.answer(text)
            time.sleep(500)
         else:
            await message.answer(text, reply_markup=buttons.application_number_phone)

@dp.message(F.content_type == types.ContentType.CONTACT)
async def handler_contant(message: Message):
   if requests.insert_user_id_in_db(message.contact.user_id, message.contact.phone_number):
      await message.answer("Спасибо! Ваш номер телефона сохранен", reply_markup=types.ReplyKeyboardRemove())
      await message.answer("Выберите раздел", reply_markup=buttons.inline_menu)

@dp.message(Command('/', 'command_admin_login'))
async def admin_login(message: Message):
   if requests.check_admin_in_db(message.from_user.id):
      await message.answer("Активирован режим Администратор", reply_markup=buttons.markup)
   else:
      if requests.insert_admin_in_db(message.from_user.id):
         await message.answer("Вы активировали режим Администратор", reply_markup=buttons.markup_admin_keyboard)
      else:
         await message.answer("Превычено количество Администраторов")

async def main() -> None:
   await dp.start_polling(bot)

if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   asyncio.run(main())