import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from bot_logic import register_handlers

logging.basicConfig(level=logging.INFO)

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID")
BASE_URL = os.environ.get("BASE_URL")  # пример: https://mft-bot.onrender.com

if not TOKEN:
    raise RuntimeError("BOT_TOKEN не задан в переменных среды")

bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
register_handlers(dp, ADMIN_CHAT_ID)

async def on_startup(app: web.Application):
    if BASE_URL:
        url = f"{BASE_URL.rstrip('/')}/webhook/{TOKEN}"
        await bot.set_webhook(url)
        logging.info(f"Webhook set to {url}")
    else:
        logging.warning("BASE_URL не задан — webhook не установлен. Задайте BASE_URL и перезапустите сервис.")

async def on_shutdown(app: web.Application):
    await bot.delete_webhook(drop_pending_updates=True)

app = web.Application()
app.router.add_get("/", lambda request: web.Response(text="OK: mft bot"))

SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=f"/webhook/{TOKEN}")
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=port)
