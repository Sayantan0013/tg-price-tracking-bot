from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from bot.keyboards.inline import get_start_keyboard

async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a button when the command /start or /help is issued."""
    user = update.effective_user
    if update.message and user:
        keyboard = get_start_keyboard()
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! I am a sample bot.",
            reply_markup=keyboard,
        )

start_handler = CommandHandler(("start", "help"), start)
