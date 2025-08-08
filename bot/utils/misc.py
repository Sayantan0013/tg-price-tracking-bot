
from bot.utils.scrapper import get_gog_game_price, get_steam_game_info, parse_steam_url, parse_gog_url
from bot.utils.constants import  CC, GOG_DEFAULT_REGION, STEAM_DEFAULT_REGION

from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from telegram import BotCommand, MenuButtonCommands
from urllib.parse import urlparse, parse_qs
from pycountry import countries


def get_country_name(alpha2_code):
    country = countries.get(alpha_2=alpha2_code)
    return country.name if country else None

def get_country_list():
    return [country.alpha_2.lower() for country in countries]

async def set_commands(application):
    commands = [
        BotCommand("start", "Check if the bot is alive"),
        BotCommand("help", "Show help info"),
        BotCommand("list", "Get Tracking List"),
        BotCommand("region", "Set your region")
    ]
    await application.bot.set_my_commands(commands)
    await application.bot.set_chat_menu_button(menu_button=MenuButtonCommands())

def get_region_from_id(tracker_id: str) -> str:
    parts = tracker_id.split("@@")
    return parts[1]


def url_switch(url,region=None):
    if "https://store.steampowered.com/" in url:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        region = region if region else STEAM_DEFAULT_REGION
        params[CC] = region
        updated_query = urlencode(params, doseq=True)

        final_url = urlunparse(parsed._replace(query=updated_query))
        game_id = parse_steam_url(final_url)
        name, price = get_steam_game_info(final_url)
        return game_id, name, price, final_url, region
    elif "https://www.gog.com/en/game/" in url:
        game_id = parse_gog_url(url)
        name, price = get_gog_game_price(url)
        return game_id, name, price, url, region if region else GOG_DEFAULT_REGION
    else:
        raise ValueError("Unsupported URL format. Only Steam and GOG URLs are supported.")