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
    file_path = f"/tmp/{message.document.file_name}"
    await message.document.download(destination=file_path)

    await state.set_state(TranslateStates.waiting_for_language)
    await state.update_data(file_path=file_path)

    await message.answer("Which language do you want me to translate the file into?")
