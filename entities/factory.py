import random
from .player import Player
from .zombie import Zombie
from settings import ZOMBIE_START_X, HEIGHT


class EntityFactory:
    WORDS = [
        "code",
        "python",
        "zombie",
        "type",
        "keyboard",
        "skill",
        "death",
    ]

    @staticmethod
    def create_player():
        return Player()

    @staticmethod
    def create_zombie(speed_min, speed_max):
        word = random.choice(EntityFactory.WORDS)
        y = random.randint(80, HEIGHT - 80)
        final_speed = random.randint(max(10, int(speed_min)), max(20, int(speed_max))) 
        return Zombie((ZOMBIE_START_X, y), word, speed=final_speed)
