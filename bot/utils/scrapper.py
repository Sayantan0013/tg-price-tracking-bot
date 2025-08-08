import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import json

from bot.utils.constants import APP, GOG, GOG_DEFAULT_REGION, STEAM, CC
from bot.utils.logger import get_logger


def parse_steam_url(url: str) -> str:
    logger = get_logger()
    
    logger.info(f"URL recieved for parsing: {url}")
    parsed = urlparse(url)

    # Extract game ID
    path_parts = parsed.path.strip("/").split("/")
    if APP in path_parts:
        game_id = path_parts[path_parts.index(APP) + 1 ]
    else:
        raise ValueError("Invalid Steam URL format. 'app' not found in path.")

    # Extract cc param
    query_params = parse_qs(parsed.query)
    cc = query_params.get(CC, [None])[0]

    # Create unified game ID
    return "@@".join([STEAM, cc, game_id])

def parse_gog_url(url: str) -> str:
    game_id = url.split("/")[-1]
    return "@@".join([GOG, GOG_DEFAULT_REGION, game_id])


def get_steam_game_info(url):
    logger = get_logger()

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')

    # Relying on the fact that the first price shown by the site is the original game price
    price_div = soup.find(lambda tag: tag.has_attr("data-price-final"))
    name_div = soup.find('div',class_='apphub_AppName')

    if price_div and name_div:
        try:
            name = name_div.text
            price_final = price_div.get("data-price-final")
            price = int(price_final) / 100

            return name, price
        except:
            raise ValueError("Unable to find game name or price")
    else:
        logger.info(f"Unable to fetch information from: {url}")

def get_epic_game_info(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        response = requests.get(url,headers=headers)
        print(response)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"

    soup = BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())
    script_tags = soup.find_all("script", type="application/ld+json")
    for tag in script_tags:
        try:
            data = json.loads(tag.string)
            if isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict) and entry.get("@id") == url:
                        print(entry)
            elif isinstance(data, dict) and data.get("@id") == url:
                print(data)
        except Exception as e:
            continue  # silently ignore invalid JSON blocks

def get_gog_game_price(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {e}"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the span by id
    try:
        price = soup.find('span', attrs={"selenium-id": "ProductFinalPrice"}).text
        name = soup.find('span', attrs={"selenium-id": "ProductTitle"}).text
        return name, float(price)
    except Exception as e:
         raise ValueError("Unable to find game name or price")


if __name__ == "__main__":
    # Example Usage:
    epic_url = "https://www.gog.com/en/game/devil_may_cry_4_special_edition?"
    get_gog_game_price(epic_url)
    # print(f"The price of the game is: {price}")
