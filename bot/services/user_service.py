from bot.utils.constants import CURRENCY, ID, PRICE, TARGET_PRICE, TRACKERS, TRACKING_HISTORY, URL, USER_DATABASE
from bot.utils.misc import get_region_from_id
from bot.utils.logger import get_logger
from bot.keyboards.inline import get_tacked_item_keyboard
from unqlite import UnQLite
from bot.config import BOT_TOKEN
from telegram import Bot
import json


async def alert(DB_PATH: str):

    bot = Bot(token=BOT_TOKEN)
    logger = get_logger()
    bot = Bot(token=BOT_TOKEN)

    with UnQLite(DB_PATH) as tracker_db, UnQLite(USER_DATABASE) as user_db:
        for user_id, user_data in user_db:
            logger.info(f'Processing user {user_id} with data {user_data}')
            user_data = json.loads(user_data.decode('utf-8'))
            trackers = user_data[TRACKERS]
            for tracker in trackers:
                tracker_id = tracker[ID]
                target_price = tracker[TARGET_PRICE]
                tracker_data = json.loads(tracker_db[tracker_id].decode('utf-8'))
                latest_price = tracker_data[TRACKING_HISTORY][-1][PRICE]
                if latest_price <= target_price:
                    region = get_region_from_id(tracker_id)
                    await bot.send_message(chat_id=user_id, 
                        text=f"Price dropped to {CURRENCY[region]}{latest_price} 🎉 for\n\n{tracker_data[URL]}",
                        reply_markup=get_tacked_item_keyboard(tracker_id))
                else:
                    logger.info(f"{user_id} Did not reach target price for user {user_id}")


if __name__ == "__main__":
    print('working')