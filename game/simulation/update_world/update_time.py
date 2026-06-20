from world.game_time import GameTime
from logger_config import get_logger
logger=get_logger(__name__)
game_time=GameTime()


def update_time():
  game_time.update_time()
  