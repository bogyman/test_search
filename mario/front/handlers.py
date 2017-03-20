
from aiohttp import web

from utils import make_request


async def search_handler(request):
    q = request.GET.get('q')
    print(q)
    if q:
        result = await make_request({'q': q}, 'front__search')
        return web.Response(text=result)
    else:
        return web.Response(text='empty q')


async def index_handler(request):
    result = await make_request('', 'front__index', nowait=True)
    return web.Response(text=result)
