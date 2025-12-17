"""
Modul Pengaturan (Settings)

Modul ini berisi semua konstanta konfigurasi untuk permainan Type Or Die.
Termasuk pengaturan layar, warna, posisi, dan parameter gameplay.
"""

WIDTH = 1920
HEIGHT = 1080
FPS = 60

BG_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)
RED = (200, 20, 20)


PLAYER_POS = (WIDTH // 2, HEIGHT - 60)
ZOMBIE_START_X = -100

INITIAL_SPAWN_INTERVAL = 2.5
MIN_SPAWN_INTERVAL = 0.5  
MIN_ZOMBIE_SPEED = 20
MAX_ZOMBIE_SPEED_CAP = 150
DIFFICULTY_SCALE_INTERVAL = 15
SPAWN_DECAY_RATE = 0.1
SPEED_INCREASE_RATE = 5
