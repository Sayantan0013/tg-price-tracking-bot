from bs4.element import PageElement
import requests
from bs4 import BeautifulSoup

def get_steam_game_price(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Relying on the fact that the first price shown by the site is the original game price
    price_div = soup.find(lambda tag: tag.has_attr("data-price-final"))

    if type(price_div) != PageElement:
        price_final = price_div["data-price-final"]
        price = int(price_final) / 100
    else:
        print("Price not found.")

    return price

if __name__ == "__main__":
    # Example Usage:
    steam_url = "https://store.steampowered.com/app/2106670/Gatekeeper/"
    price = get_steam_game_price(steam_url)
    print(f"The price of the game is: {price}")
