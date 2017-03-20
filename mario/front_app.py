from aiohttp import web
from front.handlers import index_handler, search_handler

app = web.Application()
app.router.add_get('/index', index_handler)
app.router.add_get('/search', search_handler)

web.run_app(app)