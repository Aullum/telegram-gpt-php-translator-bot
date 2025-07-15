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

async def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Register bot commands
    await application.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("restart", "Reset the translation session"),
    ])

    # Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("restart", restart_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language))

    # Set webhook
    await application.bot.set_webhook(f"{APP_URL}/webhook")

    # Aiohttp webhook app
    web_app = web.Application()
    webhook = await webhook_handler(application)
    web_app.router.add_post("/webhook", webhook)

    await application.initialize()
    await application.start()

    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    logger.info("🚀 Bot is running and listening to webhook")

if __name__ == "__main__":
    asyncio.run(main())
