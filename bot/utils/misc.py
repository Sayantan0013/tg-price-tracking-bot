
from bot.utils.scrapper import get_gog_game_price, get_steam_game_info, parse_steam_url, parse_gog_url
from bot.utils.constants import  CC, CURRENCY, DATE, DATE_FORMAT, GOG_DEFAULT_REGION, ID, PRICE, REGION, STEAM_DEFAULT_REGION, URL

from urllib.parse import urlencode, urlparse, urlunparse, parse_qs
from telegram import BotCommand, MenuButtonCommands
from urllib.parse import urlparse, parse_qs
from pycountry import countries
import matplotlib.pyplot as plt
from datetime import date, datetime
from io import BytesIO


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

async def send_tracking_history(game_id, game_db, query, context):
    tracking_data = game_db.get_tracking_history(game_id)

    if not tracking_data:
        await query.edit_message_text(text=f"No tracking data for {game_db.get_name(game_id)}")
        return

    region = get_region_from_id(game_id)
    last_price = tracking_data[-1][PRICE]

    # Append current date entry
    today_str = date.today().strftime(DATE_FORMAT)
    tracking_data.append({DATE: today_str, PRICE: last_price})


    # Parse timestamps & prices
    timestamps = [datetime.strptime(entry[DATE],DATE_FORMAT) for entry in tracking_data]
    prices = [entry[PRICE] for entry in tracking_data]

    # Create plot
    # Dark theme
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 7))
    fig.patch.set_facecolor("#1e1e1e")  # Figure background
    ax.set_facecolor("#1e1e1e")      

    plt.plot(timestamps, prices, marker="o", linestyle="-", color="#00ffcc")
    plt.xlabel("Date", color = 'white')
    plt.ylabel(f"Price {CURRENCY[region]}", color = 'white')
    plt.tight_layout()

    # Save to buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Send plot as photo
    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=buf,
        caption=f"Tracking history for {game_db.get_name(game_id)}"
    )


def url_switch(url,region=None):
    if "https://store.steampowered.com/" in url:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        region = region if region else STEAM_DEFAULT_REGION
        params[CC] = region
        updated_query = urlencode(params, doseq=True)

        final_url = urlunparse(parsed._replace(query=updated_query))
        game_id = parse_steam_url(final_url)
        data = get_steam_game_info(final_url)
        return {
            **data,
            ID: game_id, 
            URL: final_url, 
            REGION: region
        }
    elif "https://www.gog.com/en/game/" in url:
        game_id = parse_gog_url(url)
        data = get_gog_game_price(url)
        return {            
            **data,
            ID: game_id, 
            URL: url, 
            REGION: region if region else GOG_DEFAULT_REGION
        }
    else:
        raise ValueError("Unsupported URL format. Only Steam and GOG URLs are supported.")