from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler
from ..utils.validation import validate
from ..utils.misc import get_country_list,get_country_name
from ..models.user import UserDB

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # Validates if its a valid update
    await validate(update,context,query)
    user_id = update.effective_user.id

    # Handle different callback data
    if query.data == "button_clicked":
        await query.edit_message_text(text="You clicked the button! 🎉")
    elif query.data == "help_clicked":
        await query.edit_message_text(text="Accept our lord and saviour, only They can help you but if you want to track your games just drop the link 😉")
    elif query.data in get_country_list():
        user_db = UserDB()
        user_db.set_region(str(user_id), query.data)
        await query.edit_message_text(text=f"Region Set to {get_country_name(query.data)}")
        user_db.close()
    else:
        await query.edit_message_text(text="Unknow button Click")

button_handler = CallbackQueryHandler(button_callback)
