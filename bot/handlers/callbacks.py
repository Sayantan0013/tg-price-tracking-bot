from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from bot.utils.validation import validate
from bot.utils.misc import get_country_list,get_country_name
from bot.models.user import UserDB
from bot.models.game import GameDB

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # Validates if its a valid update
    validate(update,context,query).close()

    user_id = update.effective_user.id

    # Handle different callback data
    if query.data == "button_clicked":
        await query.edit_message_text(text="Pokie it hurts. Don't do it please! 🫣")
    elif query.data == "help_clicked":
        await query.edit_message_text(text="Accept our lord and saviour, only They can help you but if you want to track your games just drop the link 😉")
    elif query.data in get_country_list():
        with UserDB() as user_db:
            user_db.set_region(str(user_id), query.data)
            await query.edit_message_text(text=f"Region Set to {get_country_name(query.data)}")
    elif query.data.startswith("untrack="):
        game_id = query.data.split("=")[1]
        with UserDB() as user_db:
            user_db.remove_game_from_user(user_id, game_id)
        with GameDB() as game_db:
            await query.edit_message_text(text=f"Stopped Tracking {game_db.get_name(game_id)}")
    else:
        await query.edit_message_text(text="Unknow button Click")

button_handler = CallbackQueryHandler(button_callback)
