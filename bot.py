# bot.py

import os
import logging
import asyncio
from aiohttp import web
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers.commands import start_command, restart_command
from handlers.documents import handle_file
from handlers.language import handle_language
from webhook.server import webhook_handler

TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", 5000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_handlers(app):
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("restart", restart_command))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language))

async def run_webhook(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("restart", "Reset the translation session"),
    ])
    await app.bot.set_webhook(f"{APP_URL}/webhook")

    web_app = web.Application()
    webhook = await webhook_handler(app)
    web_app.router.add_post("/webhook", webhook)

    await app.initialize()
    await app.start()

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    logger.info(f"🚀 Webhook active at {APP_URL}/webhook")

async def run_polling(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("restart", "Reset the translation session"),
    ])
    logger.info("🤖 No APP_URL set, starting in polling mode...")
    await app.run_polling()

def main():
    if not TOKEN:
        logger.error("❌ BOT_TOKEN is not set. Please set the BOT_TOKEN environment variable.")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    register_handlers(app)

    if APP_URL:
        asyncio.run(run_webhook(app))
    else:
        app.run_polling()

if __name__ == "__main__":
    main()
