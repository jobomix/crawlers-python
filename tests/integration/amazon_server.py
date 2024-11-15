import asyncio
import pathlib

from aiohttp import web
from xtracted_common.model import amazon_url_asin_path

filepath = pathlib.Path(__file__).resolve().parent.parent

routes = web.RouteTableDef()


def get_amazon_html(path: pathlib.Path) -> web.Response:
    with open(path, 'r') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def html_response(path: pathlib.Path) -> web.Response:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, get_amazon_html, path)


@routes.get('/{name:.*}')
async def handle(request: web.Request) -> web.Response:
    name = request.match_info.get('name', 'gopro.html')
    if amazon_url_asin_path.match(f'/{name}'):
        splits = name.split('/')
        return await html_response(filepath / 'asins' / f'{splits[-1]}.html')
    else:
        raise web.HTTPNotFound()


def new_web_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    web.run_app(new_web_app())
