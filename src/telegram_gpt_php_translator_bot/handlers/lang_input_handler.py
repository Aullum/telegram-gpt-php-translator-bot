import tempfile
import os
from telegram_gpt_php_translator_bot.services.parser_service import extract_visible_text
from telegram_gpt_php_translator_bot.services.openai_service import translate_chunks
import aiofiles
import uuid
from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from .translate_handler import TranslateStates

lang_input_router = Router()


@lang_input_router.message(TranslateStates.waiting_for_language)
async def handle_lang_input(msg: types.Message, state: FSMContext):
    lang = msg.text.strip()
    data = await state.get_data()
    file_path: str = data["file_path"]
    await state.clear()

    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        html_raw = await f.read()

    replaced_html, chunks, marker_map = extract_visible_text(html_raw)

    translations = await translate_chunks(chunks, lang)

    for marker, translated in zip(marker_map.keys(), translations):
        replaced_html = replaced_html.replace(marker, translated)

    tmp_dir = tempfile.gettempdir()
    out_path = os.path.join(tmp_dir, f"translated_{uuid.uuid4().hex}.php")

    async with aiofiles.open(out_path, "w", encoding="utf-8") as f:
        await f.write(replaced_html)

    await msg.answer_document(
        types.FSInputFile(out_path), caption="✅ Here is your translated index.php"
    )
