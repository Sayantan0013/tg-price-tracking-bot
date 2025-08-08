from bot.utils.constants import DATE, DATE_FORMAT, GAME_DATABASE, NAME, PRICE, TRACKING_HISTORY, URL
from typing import List, Dict, Optional
from bot.utils.logger import get_logger
from unqlite import UnQLite
from datetime import date
import json
import os


class GameDB:
    """
    Game_ID:
        - name
        - url
        - List[ Tracking_Details ]

    Tracking_Details:
        - date
        - price
    """

    def __init__(self):

        self.db_dir = os.path.dirname(GAME_DATABASE)
        if self.db_dir:
            os.makedirs(self.db_dir, exist_ok=True)
        self.db = UnQLite(GAME_DATABASE)
        self.logger = get_logger()

    def _get_game_data(self, game_id: str) -> Dict:
        if game_id not in self.db:
            raise ValueError("Game does not exist.")
        game_data = self.db[game_id]
        return json.loads(game_data.decode("utf-8"))
    
    def get_url(self, game_id: str) -> Optional[str]:
        """Get the URL of a game."""
        game_data = self._get_game_data(game_id)
        return game_data.get(URL, None)
    def get_name(self, game_id: str) -> Optional[str]:
        game_data = self._get_game_data(game_id)
        return game_data.get(NAME, None)        


    def add_game(self, game_id: str, url: str, name: str, price: float):
        """Add a new game with no tracking history."""
        if game_id in self.db:
            self.logger.info(f"Game {game_id} already exists.")
            return
        
        self.db[game_id] = json.dumps({
            URL: url,
            NAME: name,
            TRACKING_HISTORY: [{
                DATE: date.today().strftime(DATE_FORMAT),
                PRICE: price
            }]
        })

    def add_tracking_entry(self, game_id: str, date: str, price: float):
        """Add a new tracking record to a game."""
        game_data = self._get_game_data(game_id)
        game_data[TRACKING_HISTORY].append({
            DATE: date,
            PRICE: price
        })
        self.db[game_id] = json.dumps(game_data)

    def get_tracking_history(self, game_id: str) -> List[Dict]:
        """Get all price tracking records for a game."""
        game_data = self._get_game_data(game_id)
        return game_data.get(TRACKING_HISTORY, [])
    
    def get_latest_price(self, game_id: str) -> Optional[float]:
        """Get the latest price of a game."""
        tracking_history = self.get_tracking_history(game_id)
        if tracking_history:
            return tracking_history[-1].get(PRICE)

    def get_game(self, game_id: str) -> Optional[Dict]:
        """Get the entire game record."""
        return self._get_game_data(game_id)

    def delete_game(self, game_id: str):
        """Remove a game entry entirely."""
        if game_id in self.db:
            del self.db[game_id]

    def list_all_games(self) -> List[str]:
        """List all game IDs in the database."""
        return list(self.db.keys())

    def close(self):
        self.db.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
