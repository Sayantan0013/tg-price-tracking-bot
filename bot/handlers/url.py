from telegram import Update, MessageEntity
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.utils.constants import CC, CURRENCY, GOG_DEFAULT_REGION, STEAM_DEFAULT_REGION
from bot.utils.misc import url_switch
from bot.models.user import UserDB
from bot.models.game import GameDB

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Extracts URLs from a message and sends a response.
    This handler is triggered by messages containing URLs.
    """
    message = update.message
    user_id = update.effective_user.id
    with UserDB() as user_db:
        user_region = user_db.get_region(user_id)

    if not message:
        return None

    # We can use a list to store all the URLs found in the message
    urls_found = []

    # Check for 'entities' and 'caption_entities' (for messages with media)
    entities = message.entities or message.caption_entities or []

    for entity in entities:
        if entity.type == MessageEntity.URL:
            # Extract the URL text from the message
            url = message.text[entity.offset : entity.offset + entity.length]
            urls_found.append(url)

    with UserDB() as user_db, GameDB() as game_db:
        if urls_found:
            for url in urls_found:
                game_id, name, price, final_url, region = url_switch(url,user_region)
                await message.reply_text(f"The price of the game: {CURRENCY[region]}{price}")

                user_db.add_game_to_user(user_id, game_id)
                game_db.add_game(game_id, final_url, name, price)

    # If no URLs were extracted (which shouldn't happen if the filter is working), do nothing.

# Create the handler that filters for messages containing URL entities
url_handler = MessageHandler(filters.Entity(MessageEntity.URL), handle_url)
