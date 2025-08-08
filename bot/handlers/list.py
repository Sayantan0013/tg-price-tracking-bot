from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.models.game import GameDB
from bot.models.user import UserDB
from bot.utils.constants import CURRENCY, ID, PRICE, REGION, URL
from bot.utils.logger import get_logger
from bot.utils.misc import get_region_from_id
from bot.keyboards.inline import get_tacked_item_keyboard


async def list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a button when the command /list"""

    user = update.effective_user
    logger = get_logger()

    if not update.message or not user:
        return
    
    with UserDB() as user_db:
        user_games = user_db.get_games(user.id)
        fetched_games = []

        with GameDB() as game_db:
            for game in user_games:
                game_id = game.get(ID)
                game_url = game_db.get_url(game_id)
                latest_price = game_db.get_latest_price(game_id)
                if game_url and latest_price:
                    logger.info(f"Adding {game_id} to the fetched_games ")

                    fetched_games.append({
                        URL: game_url,
                        PRICE: latest_price,
                        REGION: get_region_from_id(game_id),
                        ID: game_id
                    })
    
    await update.message.reply_html(
        f"Hi {user.mention_html()}! Here is your list of Games:",
    )
    for game in fetched_games:
        logger.info(f'Showing tracking details for the game {game[ID]}')
        await update.message.reply_html(
            f"{game[URL]} \n\nLatest Price: {CURRENCY[game[REGION]]}{game[PRICE]}",
            reply_markup=get_tacked_item_keyboard(game[ID])
            )
           

list_handler = CommandHandler(("list"), list)
