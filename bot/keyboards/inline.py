from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.constants import SUPPORTED_REGIONS
from pycountry import countries

def get_start_keyboard() -> InlineKeyboardMarkup:
    """Returns the inline keyboard for the start message."""
    keyboard = [
        [InlineKeyboardButton("👉 Poke me!", callback_data="button_clicked")],
        [InlineKeyboardButton("🤲 Help", callback_data="help_clicked")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_region_keyboard() -> InlineKeyboardMarkup:
    """Returns the inline keyboard for the start message."""
    keyboard =  [
        [
            InlineKeyboardButton(f"{countries.get(alpha_2=region).flag}", callback_data=region) for region in SUPPORTED_REGIONS
        ]
    ]

    return InlineKeyboardMarkup(keyboard)

def get_tacked_item_keyboard(game_id: list) -> InlineKeyboardMarkup:
    """Returns the inline keyboard for the tracked game."""
    keyboard = [
        [
            InlineKeyboardButton("🛑 Stop Tracking", callback_data=f"untrack={game_id}"),
            InlineKeyboardButton("📉 History", callback_data=f"history={game_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
