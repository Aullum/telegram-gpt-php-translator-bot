# handlers/commands.py

from telegram import Update
from telegram.ext import ContextTypes

# In-memory user session store
user_states = {}

def get_user_states():
    return user_states

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Responds to /start command.
    """
    await update.message.reply_text(
        "👋 Hi! Please send an `index.php` file to translate."
    )

async def restart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Clears current user's session.
    """
    user_states.pop(update.message.from_user.id, None)
    await update.message.reply_text(
        "🔄 Reset complete. Please send a new file."
    )
