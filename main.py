"""FastAPI service with Telegram polling in the same Render Web Service."""
from __future__ import annotations
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import APP_NAME, APP_ENV, BOT_TOKEN

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger("god-mode-x.api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    telegram_app = None
    if BOT_TOKEN:
        from bot import build_application
        telegram_app = build_application()
        await telegram_app.initialize()
        await telegram_app.start()
        if telegram_app.updater is None:
            raise RuntimeError("Telegram polling updater is unavailable.")
        await telegram_app.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"],
        )
        app.state.telegram_bot_running = True
        logger.info("Telegram bot polling started.")
    else:
        app.state.telegram_bot_running = False
        logger.error("BOT_TOKEN is missing. API is online, Telegram bot is OFF.")
    app.state.telegram_application = telegram_app
    try:
        yield
    finally:
        if telegram_app is not None:
            if telegram_app.updater and telegram_app.updater.running:
                await telegram_app.updater.stop()
            if telegram_app.running:
                await telegram_app.stop()
            await telegram_app.shutdown()
            logger.info("Telegram bot stopped cleanly.")

app = FastAPI(title=APP_NAME, version="0.2.0",
              description="Telegram-first creative editing platform API.",
              lifespan=lifespan)

@app.get("/")
async def home():
    running = getattr(app.state, "telegram_bot_running", False)
    return {"ok": True, "service": APP_NAME, "environment": APP_ENV,
            "version": "0.2.0", "telegram_bot": "online" if running else "offline"}

@app.get("/health")
async def health():
    running = getattr(app.state, "telegram_bot_running", False)
    return {"ok": True, "service": "api",
            "telegram_bot": "online" if running else "offline"}
