from telegram import Update, MessageEntity
from telegram.ext import ContextTypes, MessageHandler, filters
from ..services.scrapper import get_steam_game_price

def url_switch(url):
    if "https://store.steampowered.com/" in url:
        return get_steam_game_price(url)
    else:
        return "bad"

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Extracts URLs from a message and sends a response.
    This handler is triggered by messages containing URLs.
    """
    message = update.message
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

    if urls_found:
        for url in urls_found:
            await message.reply_text(f"The price of the game: ₹{url_switch(url)}")
    # If no URLs were extracted (which shouldn't happen if the filter is working), do nothing.

# Create the handler that filters for messages containing URL entities
url_handler = MessageHandler(filters.Entity(MessageEntity.URL), handle_url)
