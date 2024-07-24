import sys
import logging

from routes.server.routes import routes
from Settings.serverSttings import WEB_SERVER_HOST, WEB_SERVER_PORT

from aiohttp import web

'''
Middleware - фабрика промежуточного ПО, которая производит
промежуточное ПО, которое нормализует путь запроса. Под нормадиацией 
понимается:
    1. Добавить или удалить слеш в конце пути
    2. Двойная косая черта заменяется одной  
'''
async def cors_middleware(app, handler):
    async def middleware_handler(request):
        # Настроить CORS на принятие запросов только с определенного домена
        response = await handler(request)
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'content-type, authorization'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response 
    return middleware_handler

app = web.Application(middlewares=[cors_middleware])
app.add_routes(routes)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)