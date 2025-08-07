from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from bot.keyboards.inline import get_region_keyboard

async def region(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a button when the command /region"""
    user = update.effective_user

    if update.message and user:
        keyboard = get_region_keyboard()
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! Please select your region",
            reply_markup=keyboard,
        )

region_handler = CommandHandler(("region"), region)
