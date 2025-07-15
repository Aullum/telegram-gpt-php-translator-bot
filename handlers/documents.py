# handlers/documents.py

import os
from telegram import Update
from telegram.ext import ContextTypes
from handlers.commands import get_user_states

user_states = get_user_states()

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles uploaded document. Accepts only index.php files.
    Saves the file and updates user state.
    """
    user_id = update.message.from_user.id
    doc = update.message.document

    if not doc.file_name.endswith("index.php"):
        await update.message.reply_text("⚠️ Please upload a file named `index.php`.")
        return

    file = await doc.get_file()
    file_path = f"/tmp/{user_id}_index.php"
    await file.download_to_drive(file_path)

    user_states[user_id] = {"file_path": file_path}
    await update.message.reply_text("✅ File received. Now type the target language (e.g. English, German).")
