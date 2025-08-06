from telegram.ext import Application
from bot.config import BOT_TOKEN
from bot.handlers.start import start_handler
from bot.handlers.callbacks import button_handler
from bot.handlers.url import url_handler

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(url_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(poll_interval=100)

if __name__ == "__main__":
    main()
