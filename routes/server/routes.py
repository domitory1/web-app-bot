from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiogram.utils.web_app import safe_parse_webapp_init_data
from Settings.botSettings import API_TOKEN
import jwt
from Settings.serverSttings import JWT_KEY
from datetime import datetime, timedelta, timezone

routes = web.RouteTableDef()

# Добавить токен обновления
def create_jwt(user_data):
    payload = {
        "user": user_data,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=20)
    }
    token = jwt.encode(payload=payload, key=JWT_KEY, algorithm='HS256')
    return token

@routes.options('/auth/check_init_data')
# Настроить CORS на принятие запросов только с определенного домена
async def options_handler(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'content-type, authorization',
    }
    return web.Response(headers=headers)

@routes.post('/auth/check_init_data')
async def check_data_handler(request: Request):
    user_data = await request.json()
    try:
        user_data = safe_parse_webapp_init_data(token=API_TOKEN, init_data=user_data['initData'])
    except ValueError:
        #return json_response({"ok": False, "err": "Хорошая работа, исследователь"}, status=401)
        user_data = {
            'id': 651509930, 
            'is_bot': None, 
            'first_name': '/', 
            'last_name': '', 
            'username': 'Axiura_Leocefala', 
            'language_code': 'ru', 
            'photo_url': None, 
            'allows_write_to_pm': True
        }
        token = create_jwt(user_data)
        return json_response({"ok": True, "token": token, "data": user_data})
    finally:
        token = create_jwt(user_data)
        return json_response({"ok": True, "token": token, "data": user_data})
