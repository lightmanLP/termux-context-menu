import asyncio
import secrets
import webbrowser

from aiohttp import web
import aiosqlite

PORT = 23325
TOKEN_SIZE = 32
loop = asyncio.get_event_loop_policy().get_event_loop()
app = web.Application(loop=loop)
routes = web.RouteTableDef()
db: aiosqlite.Connection


async def init():
    global db

    db = await aiosqlite.connect("server.db")
    await db.execute("CREATE TABLE IF NOT EXISTS tokens (token TEXT PRIMARY KEY)")


async def create_token() -> str:
    token = secrets.token_urlsafe(TOKEN_SIZE)
    await db.execute("INSERT INTO tokens VALUES (?)", (token, ))
    return token


async def check(request: web.Request):
    try:
        token = request.headers["Authorization"]
        assert " " not in token
        async with db.execute("SELECT * FROM tokens WHERE token = ?", (token, )) as cur:
            async for row in cur:
                break
            else:
                raise AssertionError()
    except AssertionError:
        raise web.HTTPUnauthorized()


@routes.post("/open-url")
async def hello(request: web.Request) -> web.Response:
    await check(request)
    data = await request.json()
    webbrowser.open_new_tab(data["url"])
    return web.Response(text="ok")


async def run():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(
        runner,
        host="0.0.0.0",
        port=PORT
    )
    await site.start()
    await site._server.serve_forever()


async def shutdown():
    await db.close()


app.add_routes(routes)
