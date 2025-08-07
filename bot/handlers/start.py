from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from bot.keyboards.inline import get_start_keyboard
from bot.models.user import UserDB

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a button when the command /start or /help is issued."""
    user = update.effective_user
    user_db = UserDB()
    user_db.add_user(user.id)
    user_db.close()

    if update.message and user:
        # await user.set_menu_button(MenuButton())
        keyboard = get_start_keyboard()
        await update.message.reply_html(
            rf"Hi {user.mention_html()}! I am a sample bot that helps you track prices of your favourite Item",
            reply_markup=keyboard,
        )

start_handler = CommandHandler(("start", "help"), start)
