from aiogram import Router
from .start_handler import start_router
from .translate_handler import translate_router
from .lang_input_handler import lang_input_router

handler_router = Router()
handler_router.include_routers(
    start_router,
    translate_router,
    lang_input_router,
)
