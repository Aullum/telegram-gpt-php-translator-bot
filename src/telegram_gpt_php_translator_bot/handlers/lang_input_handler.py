import tempfile
import os
import logging
from telegram_gpt_php_translator_bot.services.parser_service import (
    extract_text_elements_from_html,
)
from telegram_gpt_php_translator_bot.services.openai_service import translate_elements
from telegram_gpt_php_translator_bot.services.parser_service import (
    apply_translations_to_html,
)
import aiofiles
from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from telegram_gpt_php_translator_bot.states import TranslateStates

lang_input_router = Router()


@lang_input_router.message(TranslateStates.waiting_for_language)
async def handle_lang_input(msg: types.Message, state: FSMContext):
    lang = msg.text.strip()
    data = await state.get_data()
    file_path: str = data["file_path"]
    await state.clear()

    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            html_raw = await f.read()

        html_with_markers, marker_map = extract_text_elements_from_html(html_raw)
        translations = await translate_elements(marker_map, lang)
        translated_html = apply_translations_to_html(html_with_markers, translations)

        tmp_out = os.path.join(tempfile.gettempdir(), f"index_{lang}.php")
        async with aiofiles.open(tmp_out, "w", encoding="utf-8") as f:
            await f.write(translated_html)

        await msg.answer_document(
            types.FSInputFile(tmp_out), caption=f"✅ Translated to {lang}"
        )

    except Exception as e:
        await msg.answer(f"❌ Translation failed: {e}")

    finally:
        for path in [file_path, tmp_out]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as e:
                    logging.warning(f"Failed to delete temp file {path}: {e}")
