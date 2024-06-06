from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiogram.utils.web_app import safe_parse_webapp_init_data

from Settings.botSettings import API_TOKEN

routes = web.RouteTableDef()

@routes.options('/auth/check_init_data')
async def options_handler(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'content-type',
    }
    return web.Response(headers=headers)

@routes.post('/auth/check_init_data')
async def check_data_handler(request: Request):
    data = await request.json()
    try:
        data = safe_parse_webapp_init_data(token=API_TOKEN, init_data=data['initData'])
    except ValueError:
        return json_response({"ok": False, "err": "Хорошая работа, исследователь"}, status=401)
    return json_response({"ok": True, "data": data.user.dict()})
