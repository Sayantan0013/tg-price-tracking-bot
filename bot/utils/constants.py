from babel.numbers import get_currency_symbol

USER_DATABASE= "data/user.unqlite"
STEAM_DATABASES={
    'in': "data/steam/in.unqlite",
    'tr': "data/steam/tr.unqlite"
}
EPIC_DATABASE="data/epic.unqlite"

REGION="region"
ID="id"
GAMES="games"
URL="url"
CC="cc"

CURRENCY= {
    'in': get_currency_symbol('INR'),
    'tr': get_currency_symbol('USD')
}
