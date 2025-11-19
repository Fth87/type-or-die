import os

# Use dummy SDL driver for headless testing
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from entities.zombie import Zombie


def test_zombie_typing_progress():
    pygame.init()
    z = Zombie((0, 0), "abc", speed=1)
    assert not z.is_dead()
    assert z.type_char("a")
    assert z.progress == 1
    assert z.type_char("b")
    assert z.type_char("c")
    assert z.is_dead()
    pygame.quit()
