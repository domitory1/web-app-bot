import asyncio
import logging
import ssl
import sys
import time

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import FSInputFile, Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from aiohttp import web

from Secrets.botSettings import *
from Secrets.webserverSettings import *
import Buttons.buttons as buttons
import Requests.requests as requests

dp = Dispatcher()

@dp.message(CommandStart())
async def start_command(message: Message) -> None:
   message_texts_start = [
      "Добрый день! 😊", 
      "Перед тем, как вы сделаете ваш первый заказ, поделитесь, пожалуйста, своим номером телефона. 😌\n"
      "Он нужен для того, чтобы мы смогли добавить блюда именно в вашу корзину"
   ]
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
async def handler_contant(message: Message) -> None:
   if requests.insert_user_id_in_db(message.contact.user_id, message.contact.phone_number):
      await message.answer("Спасибо! Ваш номер телефона сохранен", reply_markup=types.ReplyKeyboardRemove())
      await message.answer("Выберите раздел", reply_markup=buttons.inline_menu)

@dp.message(Command('/', 'command_admin_login'))
async def admin_login(message: Message) -> None:
   if requests.check_admin_in_db(message.from_user.id):
      await message.answer("Активирован режим Администратор", reply_markup=buttons.markup)
   else:
      if requests.insert_admin_in_db(message.from_user.id):
         await message.answer("Вы активировали режим Администратор", reply_markup=buttons.markup_admin_keyboard)
      else:
         await message.answer("Превычено количество Администраторов") 

async def on_startup(bot: Bot) -> None:
   await bot.set_webhook(
      f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}",
      certificate=FSInputFile(WEBHOOK_SSL_CERT),
      secret_token=WEBHOOK_SECRET,
   )

async def main() -> None:
   # Регистрация запуска хука, чтобы инициализировать вебхук
   dp.startup.register(on_startup)

   # Инициализация экземпляра бота с режимом разбора по умолчанию, 
   # который будет передаваться во всех вызовах API
   bot = Bot(API_TOKEN,  parse_mode=ParseMode.HTML)

   # Создание экземпляра aiohttp.web.Application
   app = web.Application()
   
   # Создание экземпляра обработчика запросов для одного бота
   webhook_request_handle = SimpleRequestHandler(
      dispatcher=dp,
      bot=Bot,
      secret_token=WEBHOOK_SECRET,
   )

   # Регистрация обаботчика вебхука на приложении
   webhook_request_handle.register(app, path=WEBHOOK_PATH)

   # Привязка диспетчера к запуску и остановка aiohttp-приложения
   setup_application(app, dp, bot=bot)

   # Генерация SSL-контекста
   context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
   context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

   # Запуск вебсервера
   web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT, ssl_context=context) # 

   # Запуск полигонации сервера телеграм
   await dp.start_polling(bot)

if __name__ == "__main__":
   logging.basicConfig(level=logging.INFO, stream=sys.stdout)
   asyncio.run(main())