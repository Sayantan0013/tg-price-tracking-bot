from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_start_keyboard() -> InlineKeyboardMarkup:
    """Returns the inline keyboard for the start message."""
    keyboard = [
        [InlineKeyboardButton("Click me!", callback_data="button_clicked")],
        [InlineKeyboardButton("Help", callback_data="help_clicked")],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_region_keyboard() -> InlineKeyboardMarkup:
    """Returns the inline keyboard for the start message."""
    keyboard =  [
        [InlineKeyboardButton("Turkey 🇹🇷", callback_data="tr")],
        [InlineKeyboardButton("India 🇮🇳", callback_data="in")]
    ]

    return InlineKeyboardMarkup(keyboard)
