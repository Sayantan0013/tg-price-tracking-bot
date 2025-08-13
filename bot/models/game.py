from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from bot.utils.constants import DATE, DATE_FORMAT, GAME_DATABASE, ID, NAME, PRICE, TRACKING_HISTORY, URL
from bot.utils.logger import get_logger
from unqlite import UnQLite
import json
import os


class TrackingHistory(BaseModel):
    date: str = Field(..., alias=DATE)
    price: float = Field(..., alias=PRICE)

    class Config:
        validate_by_name = True
        extra = "ignore"


class Game(BaseModel):
    name: str = Field(..., alias=NAME)
    url: str = Field(..., alias=URL)
    tracking_history: List[TrackingHistory] = Field(default_factory=list, alias=TRACKING_HISTORY)

    class Config:
        validate_by_name = True
        extra = "ignore"


class GameDB:
    """
    Game_ID:
        - name
        - url
        - List[TrackingHistory]

    TrackingHistory:
        - date
        - price
    """

    def __init__(self):
        self.db_dir = os.path.dirname(GAME_DATABASE)
        if self.db_dir:
            os.makedirs(self.db_dir, exist_ok=True)
        self.db = UnQLite(GAME_DATABASE)
        self.logger = get_logger()

    def _get_game_data(self, game_id: str) -> Game:
        if game_id not in self.db:
            raise ValueError("Game does not exist.")
        game_data = json.loads(self.db[game_id].decode("utf-8"))
        return Game.model_validate(game_data)

    def get_url(self, game_id: str) -> Optional[str]:
        return self._get_game_data(game_id).url

    def get_name(self, game_id: str) -> Optional[str]:
        return self._get_game_data(game_id).name

    def add_game(self, data: dict) -> bool:
        """Add a new game with an initial tracking entry."""
        game_id = data.get(ID)
        if not game_id:
            self.logger.info(f"No Game id found in {data}")
            return False

        if game_id in self.db:
            self.logger.info(f"Game {game_id} already exists.")
            return False

        tracking_history = TrackingHistory.model_validate(data)
        tracking_history.date = date.today().strftime(DATE_FORMAT)
        game = Game.model_validate(data)
        game.tracking_history.append(tracking_history)

        self.db[data[ID]] = game.model_dump_json(by_alias=True)

        return True

    def add_tracking_entry(self, data: dict) -> bool:
        game_id = data.get(ID)
        if not game_id:
            self.logger.info(f"No Game id found in {data}")
            return False

        game = self._get_game_data(game_id)
        game.tracking_history.append(TrackingHistory.model_validate(data))
        self.db[game_id] = game.model_dump_json(by_alias=True)

        return True

    def get_tracking_history(self, game_id: str) -> List[TrackingHistory]:
        return self._get_game_data(game_id).tracking_history

    def get_latest_price(self, game_id: str) -> Optional[float]:
        tracking_history = self.get_tracking_history(game_id)
        return tracking_history[-1].price if tracking_history else None

    def get_game(self, game_id: str) -> Game:
        return self._get_game_data(game_id)

    def delete_game(self, game_id: str):
        if game_id in self.db:
            del self.db[game_id]

    def list_all_games(self) -> List[str]:
        return list(self.db.keys())

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
