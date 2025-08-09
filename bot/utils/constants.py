from babel.numbers import get_currency_symbol
from pycountry import currencies, countries


USER_DATABASE="data/user.unqlite"
GAME_DATABASE="data/games.unqlite"
LOG_FILE="logs/debug.log"

STORE="store"
URL="url"
DATE_FORMAT="%d %B %Y"
REGION="region"
PRICE="price"
ID="id"
NAME="name"
TRACKERS="trackers"
TRACKING_HISTORY="tracking_history"
DATE="date"
URL="url"
CC="cc"
APP="app"
STEAM="steam"
GOG="gog"
EPIC="epic"
TARGET_PRICE="target_price"

SUPPORTED_REGIONS = ['us', 'in', 'tr', 'ch']
STEAM_DEFAULT_REGION= "in"
GOG_DEFAULT_REGION="us"

CURRENCY= {
    region: get_currency_symbol(
                currencies.get(numeric=
                    countries.get(alpha_2=
                        region.upper()).numeric, 
                    default= currencies.get(numeric='840')).alpha_3) 
    for region in SUPPORTED_REGIONS
}