import os
import tempfile
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

translate_router = Router()


class TranslateStates(StatesGroup):
    waiting_for_language = State()
    file_path = State()


@translate_router.message(
    lambda msg: msg.document and msg.document.file_name.endswith("index.php")
)
async def receive_file(message: types.Message, state: FSMContext):
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, message.document.file_name)

    file = await message.bot.get_file(message.document.file_id)
    await message.bot.download_file(file.file_path, destination=file_path)

    await state.set_state(TranslateStates.waiting_for_language)
    await state.update_data(file_path=file_path)

    await message.answer("Which language do you want me to translate the file into?")
