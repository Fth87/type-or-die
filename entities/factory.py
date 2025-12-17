import random
from .player import Player
from .zombie import Zombie
from settings import ZOMBIE_START_X, HEIGHT
import json


class EntityFactory:
    """
    Pabrik (Factory) untuk membuat entitas game (Player, Zombie).
    
    Menggunakan pola desain Factory untuk memisahkan logika pembuatan objek.
    """
    with open('assets/static/indonesian.json', 'r') as f:
        data = json.load(f)
    WORDS = data['words']

    @staticmethod
    def create_player():
        """
        Membuat instance Player baru.

        Returns:
            Player: Objek pemain baru.
        """
        return Player()

    @staticmethod
    def create_zombie(speed_min, speed_max):
        """
        Membuat instance Zombie baru dengan parameter acak.

        Args:
            speed_min (int): Batas bawah kecepatan zombie.
            speed_max (int): Batas atas kecepatan zombie.

        Returns:
            Zombie: Objek zombie baru dengan kata dan posisi acak.
        """
        word = random.choice(EntityFactory.WORDS)
        y = random.randint(80, HEIGHT - 80)
        final_speed = random.randint(max(10, int(speed_min)), max(20, int(speed_max))) 
        return Zombie((ZOMBIE_START_X, y), word, speed=final_speed)
