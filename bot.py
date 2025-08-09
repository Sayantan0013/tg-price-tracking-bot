from telegram.ext import Application
from bot.config import BOT_TOKEN
from bot.handlers.start import start_handler
from bot.handlers.callbacks import button_handler
from bot.handlers.url import url_conversation_handler
from bot.handlers.region import region_handler
from bot.handlers.list import list_handler
from bot.utils.constants import GAME_DATABASE
from bot.utils.logger import get_logger
from bot.utils.misc import set_commands
from bot.services.tracking_service import track
from bot.services.user_service import alert

from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import gc
import sys


async def periodic_task(context):
    logger = get_logger()
    # seen_ids = set()
    # for obj in gc.get_objects():
    #     if id(obj) not in seen_ids:
    #         seen_ids.add(id(obj))
    #         print(repr(type(obj)), sys.getsizeof(obj))
    for name, obj in globals().items():
        print(f"Variable '{name}': Type={type(obj)}, Size={sys.getsizeof(obj)} bytes")

def main() -> None:
    """Run the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    # application.job_queue.run_repeating(periodic_task, interval= 5)

    # Register handlers
    application.add_handler(start_handler)
    application.add_handler(button_handler)
    application.add_handler(url_conversation_handler)
    application.add_handler(region_handler)
    application.add_handler(list_handler)

    set_commands(application).close()
    # Run the bot until the user presses Ctrl-C
    application.run_polling(poll_interval = 0)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(track, 'cron', args=(GAME_DATABASE,), hour=12)
    scheduler.add_job(lambda: asyncio.run(alert(GAME_DATABASE)), 'cron', hour=13)

    scheduler.start()

    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        print('Stopping schedulers')
        scheduler.shutdown()
