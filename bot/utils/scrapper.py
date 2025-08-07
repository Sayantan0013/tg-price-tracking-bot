import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_steam_game_info(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

    path = urlparse(url).path
    segments = path.strip("/").split("/")

    if len(segments) >= 2 and segments[0] == "app":
        game_id = segments[1]
    else:
        raise ValueError("Game Id Not found")

    soup = BeautifulSoup(response.text, 'html.parser')

    # Relying on the fact that the first price shown by the site is the original game price
    price_div = soup.find(lambda tag: tag.has_attr("data-price-final"))

    if price_div:
        try:
            price_final = price_div.get("data-price-final")
            price = int(price_final) / 100
        except:
            print('Sorry Guys')
    else:
        print("Price not found.")

    return game_id, price

if __name__ == "__main__":
    # Example Usage:
    steam_url = "https://store.steampowered.com/app/2106670/Gatekeeper/"
    game_id, price = get_steam_game_info(steam_url)
    print(f"The price of the game {game_id} is: {price}")
