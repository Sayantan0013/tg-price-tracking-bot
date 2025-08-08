import os
from unqlite import UnQLite
from bot.utils.constants import TRACKERS, ID, TARGET_PRICE, USER_DATABASE, REGION
from typing import List, Dict, Optional
from bot.utils.logger import get_logger
import json

class UserDB:
    """
        User_ID:
            - region
            - List[ Tracker ]

        Tracker:
            - id
            - min_price
    """
    def __init__(self):
            self.db_dir = os.path.dirname(USER_DATABASE)
            if self.db_dir:
                os.makedirs(self.db_dir, exist_ok=True)
            self.db = UnQLite(USER_DATABASE)
            self.logger = get_logger()

    def _get_user_data(self, user_id: int):
        if user_id not in self.db:
            raise ValueError("User does not exists.")
        user_data = self.db[user_id]
        return json.loads(user_data.decode('utf-8'))

    def add_user(self, user_id: int):
        """Add a new user with a region and empty game list."""
        if user_id in self.db:
            self.logger.info(f"User {user_id} already exists.")
            return
        self.db[user_id] = {}

    def set_region(self, user_id: int, region: str):
        user_data = self._get_user_data(user_id)
        user_data[REGION] = region
        self.db[user_id] = json.dumps(user_data)

    def get_region(self, user_id):
        user_data = self._get_user_data(user_id)
        return user_data.get(REGION,None)

    def get_user(self, user_id: int) -> Optional[Dict]:
        return self._get_user_data(user_id)

    def get_games(self, user_id: int) -> List[Dict]:
        """Get the list of games tracked by a user."""
        user_data = self._get_user_data(user_id)
        return user_data.get(TRACKERS, [])

    def delete_user(self, user_id: str):
        """Remove a user and their game trackers."""
        if user_id in self.db:
            del self.db[user_id]

    def add_game_to_user(self, user_id: int, game_id: str, target_price: float):
        """Add a game to a user's game tracker list."""
        user_data = self._get_user_data(user_id)

        # Prevent duplicate game ID
        if user_data.get(TRACKERS):
            if any(g[ID] == game_id for g in user_data[TRACKERS]):
                self.logger.info(f"Game {game_id} already tracked by user {user_id}.")
                return
        else:
            user_data[TRACKERS] = []

        user_data[TRACKERS].append({
            ID: game_id,
            TARGET_PRICE: target_price - 1e-4 # small trick to reduce redundant notification
        })

        self.db[user_id] = json.dumps(user_data)  # Save changes

    def remove_game_from_user(self, user_id: int, game_id: str):
        """Remove a tracked game from a user."""
        user_data = self._get_user_data(user_id)

        user_data[TRACKERS] = list(filter(lambda g: g[ID] != game_id, user_data[TRACKERS]))
        self.db[user_id] = json.dumps(user_data)

    def list_users_by_region(self, region: str) -> List[str]:
        """Get all user IDs in a specific region."""
        return [key for key in self.db if self.db[key].get(REGION) == region]

    def list_all_users(self) -> List[str]:
        return list(self.db.keys())

    def set_target_price(self, user_id, game_id, target_price):
        self.remove_game_from_user(user_id,game_id)
        self.add_game_to_user(user_id,game_id,target_price)

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
