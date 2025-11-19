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
    def create_zombie():
        word = random.choice(EntityFactory.WORDS)
        y = random.randint(80, HEIGHT - 80)
        return Zombie((ZOMBIE_START_X, y), word, speed=random.randint(40, 100))
