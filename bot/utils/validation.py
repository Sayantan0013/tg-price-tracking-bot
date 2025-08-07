async def validate(update, context, query):
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
