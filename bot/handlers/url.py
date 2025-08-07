from telegram import Update, MessageEntity
from telegram.ext import ContextTypes, MessageHandler, filters

from bot.utils.constants import CC, CURRENCY
from bot.utils.scrapper import get_steam_game_info
from bot.models.user import UserDB
from urllib.parse import urlencode

def url_switch(url,region=None):
    if "https://store.steampowered.com/" in url:
        params = {}
        if region:
            params[CC] = region
        query_string = urlencode(params)
        return get_steam_game_info(f"{url}?{query_string}")
    else:
        return "bad"

def get_currency(region=None):
    return "₹" if region == None or region not in CURRENCY.keys() else CURRENCY[region]

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Extracts URLs from a message and sends a response.
    This handler is triggered by messages containing URLs.
    """
    message = update.message
    user_id = update.effective_user.id
    user_db = UserDB()
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

    if urls_found:
        for url in urls_found:
            game_id, price = url_switch(url,user_region)
            await message.reply_text(f"The price of the game {game_id}: {get_currency(user_region)}{price}")
            # user_db.add_game_to_user()

    # If no URLs were extracted (which shouldn't happen if the filter is working), do nothing.
    user_db.close()

# Create the handler that filters for messages containing URL entities
url_handler = MessageHandler(filters.Entity(MessageEntity.URL), handle_url)
