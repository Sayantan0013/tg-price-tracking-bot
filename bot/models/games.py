import os
import json
from typing import List, Dict, Optional
from unqlite import UnQLite
from bot.utils.logger import get_logger

GAME_DATABASE = "path/to/game_database.db"

class GameDB:
    """
    Game_ID:
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

    def add_game(self, game_id: str, url: str):
        """Add a new game with no tracking history."""
        if game_id in self.db:
            self.logger.info(f"Game {game_id} already exists.")
            return
        self.db[game_id] = json.dumps({
            "url": url,
            "tracking": []
        })

    def add_tracking_entry(self, game_id: str, date: str, price: float):
        """Add a new tracking record to a game."""
        game_data = self._get_game_data(game_id)
        game_data["tracking"].append({
            "date": date,
            "price": price
        })
        self.db[game_id] = json.dumps(game_data)

    def get_tracking_history(self, game_id: str) -> List[Dict]:
        """Get all price tracking records for a game."""
        game_data = self._get_game_data(game_id)
        return game_data.get("tracking", [])

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
