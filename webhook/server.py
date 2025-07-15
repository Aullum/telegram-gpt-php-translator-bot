# webhook/server.py

from aiohttp import web
from telegram import Update

async def webhook_handler(application):
    async def handler(request):
        try:
            data = await request.json()
            update = Update.de_json(data, application.bot)
            await application.update_queue.put(update)
        except Exception as e:
            application.logger.warning(f"Webhook error: {e}")
        return web.Response(text="ok")

    return handler
