from telegram.ext import Application
from bot.config import BOT_TOKEN
from bot.handlers.start import start_handler
from bot.handlers.callbacks import button_handler
from bot.handlers.url import url_handler
from bot.handlers.region import region_handler
from bot.handlers.list import list_handler
from bot.utils.constants import GAME_DATABASE
from bot.utils.misc import set_commands
from bot.services.tracking_service import track
from bot.services.user_service import alert

from apscheduler.schedulers.background import BackgroundScheduler
import asyncio



def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    # Register handlers
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(url_handler)
    application.add_handler(region_handler)
    application.add_handler(list_handler)

    set_commands(application).close()
    # Run the bot until the user presses Ctrl-C
    application.run_polling(poll_interval = 0)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # scheduler.add_job(track, 'interval', args=(GAME_DATABASE,), minutes=1)
    # scheduler.add_job(lambda: asyncio.run(alert(GAME_DATABASE)), 'interval', minutes=1)

    scheduler.start()

    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('Stopping schedulers')
        scheduler.shutdown()
