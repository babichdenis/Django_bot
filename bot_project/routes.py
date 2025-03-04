from aiohttp import web
from handlers import handle_index, handle_category, send_welcome, check_data_handler
from aiogram.filters import Command

def setup_routes(app: web.Application, dp):
    app.add_routes([
        web.get('/', handle_index),
        web.get('/category/{category_id}', handle_category),
        web.post('/check_data', check_data_handler),  
    ])
    dp.message.register(send_welcome, Command(commands=['start']))
