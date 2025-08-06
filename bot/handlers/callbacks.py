from telegram import Update
from telegram.ext import ContextTypes, CallbackQueryHandler

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # Check if the query is None
    if query is None:
        # Optionally log the issue or notify the user
        if update.effective_chat:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Something went wrong. No callback query found."
            )
        return

    try:
        # You must answer the callback query
        await query.answer()
    except Exception as e:
        # Catch and optionally log the error
        print(f"Error answering callback query: {e}")
        return

    # Handle different callback data
    if query.data == "button_clicked":
        await query.edit_message_text(text="You clicked the button! 🎉")
    elif query.data == "help_clicked":
        await query.edit_message_text(text="This is the help text. You can add more info here.")
    else:
        await query.edit_message_text(text="Unknown action.")

button_handler = CallbackQueryHandler(button_callback)
