from bot.utils.constants import CURRENCY, DATE, GAME_DATABASE, PRICE, TRACKING_HISTORY, URL, DATE_FORMAT
from bot.utils.misc import get_region_from_id, url_switch
from bot.utils.logger import get_logger
from unqlite import UnQLite
from datetime import date
import json


def track(DB_PATH: str):
    logger = get_logger()
    with UnQLite(DB_PATH) as db:
        for key, value in db:
            value = json.loads(value.decode("utf-8"))
            id, name, price, url, region = url_switch(value[URL], get_region_from_id(key))
            latest_price = value[TRACKING_HISTORY][-1][PRICE]
            if latest_price != price:
                value[TRACKING_HISTORY].append({
                    DATE: date.today().strftime(DATE_FORMAT),
                    PRICE: price
                })
                db[key] = json.dumps(value)
                logger.info(f"Updated {key} with new price {CURRENCY[region]}{price}")
            else:
                logger.info(f"No price change for {key}. Current price is {CURRENCY[region]}{latest_price}.")


if __name__ == "__main__":
    track(GAME_DATABASE)
