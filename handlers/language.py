# handlers/language.py

import os
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from handlers.commands import get_user_states
from services.chunker import smart_split_large
from services.translator import translate_large_chunk

user_states = get_user_states()


async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles the language input from user and performs translation.
    """
    user_id = update.message.from_user.id
    if user_id not in user_states:
        await update.message.reply_text("⚠️ Please send an `index.php` file first.")
        return

    lang = update.message.text.strip()
    file_path = user_states[user_id]["file_path"]
    out_path = f"/tmp/{user_id}_translated.php"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if not content.strip():
            await update.message.reply_text("❌ File is empty or unreadable.")
            return

        chunks = smart_split_large(content, max_chunk_len=8000)
        translated_parts = []

        await update.message.reply_text(
            f"🔄 File split into {len(chunks)} parts. Starting translation..."
        )
        sizes_info = ", ".join([f"{i+1}:{len(c)//1000}k" for i, c in enumerate(chunks)])
        await update.message.reply_text(f"📊 Part sizes: {sizes_info}")

        milestones = [int(len(chunks) * x) for x in [0.25, 0.5, 0.8]]
        milestones = sorted(set(milestones) | {len(chunks)})

        for i, chunk in enumerate(chunks, 1):
            translated = await translate_large_chunk(chunk, lang, i, len(chunks))
            translated_parts.append(translated)
            if i in milestones:
                percent = int(i / len(chunks) * 100)
                await update.message.reply_text(
                    f"✅ {percent}% completed ({i}/{len(chunks)})"
                )
            if i < len(chunks):
                await asyncio.sleep(3)

        translated_full = "".join(translated_parts)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(translated_full)

        with open(out_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=f"index_{lang.lower().replace(' ', '_')}.php",
                caption=f"✅ Translation to {lang} completed!",
            )

        await update.message.reply_text("✅ Done! You can now send another file.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error occurred: {str(e)}")
    finally:
        for path in (file_path, out_path):
            if os.path.exists(path):
                os.remove(path)
        user_states.pop(user_id, None)
