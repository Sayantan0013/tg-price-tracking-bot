import os
from unqlite import UnQLite
from pydantic import BaseModel, Field
from bot.utils.constants import TRACKERS, ID, TARGET_PRICE, USER_DATABASE, REGION
from typing import List, Optional
from bot.utils.logger import get_logger
import json


class Tracker(BaseModel):
    id: str = Field(..., alias=ID)
    target_price: Optional[float] = Field(None, alias=TARGET_PRICE)

    class Config:
        validate_by_name = True
        extra = "ignore"


class User(BaseModel):
    region: Optional[str] = Field(None, alias=REGION)
    trackers: List[Tracker] = Field(default_factory=list, alias=TRACKERS)

    class Config:
        validate_by_name = True
        extra = "ignore"


class UserDB:
    """
    Structure:
        - user_id (key)
        - region
        - trackers: List[Tracker]
    """

    def __init__(self):
        self.db_dir = os.path.dirname(USER_DATABASE)
        if self.db_dir:
            os.makedirs(self.db_dir, exist_ok=True)
        self.db = UnQLite(USER_DATABASE)
        self.logger = get_logger()

    def _get_user(self, user_id: str) -> User:
        """Fetch and validate user data as Pydantic model."""
        if user_id not in self.db:
            raise ValueError("User does not exist.")
        user_data = json.loads(self.db[user_id].decode("utf-8"))
        return User.model_validate(user_data)

    def add_user(self, user_id: str):
        """Add a new user with an optional region and empty trackers list."""
        if user_id in self.db:
            self.logger.info(f"User {user_id} already exists.")
            return

        user = User.model_validate({})
        self.db[user_id] = user.model_dump_json(by_alias=True)

    def set_region(self, user_id: str, region: str):
        user = self._get_user(user_id)
        user.region = region
        self.db[user_id] = user.model_dump_json(by_alias=True)

    def get_region(self, user_id: str) -> Optional[str]:
        return self._get_user(user_id).region

    def get_user(self, user_id: str) -> User:
        return self._get_user(user_id)

    def get_trackers(self, user_id: str) -> List[Tracker]:
        """Return all trackers for the user."""
        return self._get_user(user_id).trackers

    def delete_user(self, user_id: str):
        if user_id in self.db:
            del self.db[user_id]

    def add_game_to_user(self, user_id: str, data: dict):
        user = self._get_user(user_id)
        game_id = data[ID]

        # Prevent duplicate game
        if any(tr.id == game_id for tr in user.trackers):
            self.logger.info(f"Game {game_id} already tracked by user {user_id}.")
            return

        user.trackers.append(Tracker.model_validate(data))
        self.db[user_id] = user.model_dump_json(by_alias=True)

    def remove_game_from_user(self, user_id: str, game_id: str):
        user = self._get_user(user_id)
        user.trackers = [t for t in user.trackers if t.id != game_id]
        self.db[user_id] = user.model_dump_json(by_alias=True)

    def set_target_price(self, user_id: str, game_id: str, target_price: float):
        """Update target price by replacing the tracker."""
        user = self._get_user(user_id)
        user.trackers = [t for t in user.trackers if t.id != game_id]
        user.trackers.append(Tracker(id=game_id, target_price=target_price))
        self.db[user_id] = user.model_dump_json(by_alias=True)

    def list_users_by_region(self, region: str) -> List[str]:
        """Return all user IDs in a specific region."""
        return [
            key for key in self.db.keys()
            if json.loads(self.db[key].decode("utf-8")).get(REGION) == region
        ]

    def list_all_users(self) -> List[str]:
        return list(self.db.keys())

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
