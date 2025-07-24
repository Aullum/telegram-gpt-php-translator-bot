from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from .translate_handler import TranslateStates

lang_input_router = Router()


@lang_input_router.message(TranslateStates.waiting_for_language)
async def handle_lang_input(message: types.Message, state: FSMContext):
    lang_input = message.text.strip()

    data = await state.get_data()
    file_path = data.get("file_path")

    await state.clear()

    await message.answer(
        f"✅ Got it! Target language: <b>{lang_input}</b>\nProcessing <code>{file_path}</code>..."
    )
