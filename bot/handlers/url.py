from telegram import Update, MessageEntity
from telegram.ext import ContextTypes, MessageHandler, filters, ConversationHandler, CommandHandler
from telegram.helpers import escape_markdown

from bot.utils.constants import CURRENCY, ID, NAME, REGION, URL
from bot.utils.misc import url_switch
from bot.models.user import UserDB
from bot.models.game import GameDB

WAITING_FOR_PRICE = 1  # Conversation state

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Extracts URLs from a message, sends current price, and asks for target price.
    """
    message = update.message
    user_id = update.effective_user.id
    with UserDB() as user_db:
        user_region = user_db.get_region(user_id)

    if not message:
        return ConversationHandler.END

    urls_found = []
    entities = message.entities or message.caption_entities or []

    for entity in entities:
        if entity.type == MessageEntity.URL:
            url = message.text[entity.offset : entity.offset + entity.length]
            urls_found.append(url)

    if urls_found:
        with UserDB() as user_db, GameDB() as game_db:
            # For simplicity, handle only the first URL
            url = urls_found[0]
            game_id, name, price, final_url, region = url_switch(url, user_region)

            await message.reply_text(
                f"Current price of <b>{name}</b>: {CURRENCY[region]}{price}\n"
                "What target price do you want to set?",
                parse_mode="HTML"
            )

            # Save game info in context to use later
            context.user_data["pending_game"] = {
                ID: game_id,
                NAME: name,
                URL: final_url,
                REGION: region
            }

            user_db.add_game_to_user(user_id, game_id, price)
            game_db.add_game(game_id, final_url, name, price)

        return WAITING_FOR_PRICE

    return ConversationHandler.END


async def set_target_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Stores the target price for the game.
    """
    try:
        target_price = float(update.message.text)
    except ValueError:
        await update.message.reply_text("Please enter a valid number for the target price.")
        return WAITING_FOR_PRICE

    user_id = update.effective_user.id
    game_info = context.user_data.get("pending_game")

    if not game_info:
        await update.message.reply_text("No game found in your session. Please send the link again.")
        return ConversationHandler.END

    with UserDB() as user_db:
        user_db.set_target_price(user_id, game_info[ID], target_price)

    await update.message.reply_text(
        f"✅ Target price for <b>{game_info[NAME]}</b> set to {CURRENCY[game_info[REGION]]}{target_price}.",
        parse_mode="HTML"
    )

    # Clean up stored game info
    context.user_data.pop("pending_game", None)

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Target price setup cancelled.")
    return ConversationHandler.END


# Create ConversationHandler
url_conversation_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.Entity(MessageEntity.URL), handle_url)],
    states={
        WAITING_FOR_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_target_price)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
