from aiohttp import web
import asyncio

async def handle(request):
    return web.Response(text="✅ Бот работает", headers={'ngrok-skip-browser-warning': '1'})

app = web.Application()
app.router.add_get('/', handle)

if __name__ == "__main__":
    web.run_app(app, port=8080)