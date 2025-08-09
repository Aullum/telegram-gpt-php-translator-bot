import tempfile
import os
import logging
from typing import Optional

import aiofiles
from aiogram import types, Router
from aiogram.fsm.context import FSMContext

from telegram_gpt_php_translator_bot.states import TranslateStates
from telegram_gpt_php_translator_bot.services.parser_service import (
    extract_text_elements_from_html,
    apply_translations_to_html,
)
from telegram_gpt_php_translator_bot.services.openai_service import translate_elements
from telegram_gpt_php_translator_bot.services.progress_service import ProgressUI

lang_input_router = Router()


@lang_input_router.message(TranslateStates.waiting_for_language)
async def handle_lang_input(msg: types.Message, state: FSMContext):
    lang = msg.text.strip()
    data = await state.get_data()
    file_path: str = data["file_path"]
    await state.clear()

    progress = ProgressUI(bot=msg.bot, chat_id=msg.chat.id)
    tmp_out: Optional[str] = None

    try:
        await progress.start(stage="Parsing", percent=0)

        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            html_raw = await f.read()

        html_with_markers, marker_map = extract_text_elements_from_html(html_raw)
        await progress.update(stage="Chunking", percent=20)

        translations = await translate_elements(
            marker_map,
            lang,
            progress=progress,
        )

        translated_html = apply_translations_to_html(html_with_markers, translations)
        await progress.update(stage="Saving", percent=90)

        tmp_out = os.path.join(tempfile.gettempdir(), f"index_{lang}.php")
        async with aiofiles.open(tmp_out, "w", encoding="utf-8") as f:
            await f.write(translated_html)

        await progress.update(stage="Uploading", percent=95)

        await msg.answer_document(
            types.FSInputFile(tmp_out), caption=f"✅ Translated to {lang}"
        )
        await progress.done()

        await msg.answer(
            "Ready for the next translation. Send me an index.php file to start translation."
        )

    except Exception as e:
        await progress.fail(f"Telegram server says - {e}")
        await msg.answer(
            "Ready for the next translation. Send me an index.php file to start translation."
        )

    finally:
        for path in [file_path, tmp_out]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception as ex:
                    logging.warning(f"Failed to delete temp file {path}: {ex}")
