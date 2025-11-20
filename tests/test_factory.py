import os

# Use dummy SDL driver for headless testing
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pytest
import pygame

from entities.factory import EntityFactory
from entities.player import Player
from entities.zombie import Zombie


def test_create_player():
    pygame.init()
    player = EntityFactory.create_player()
    assert isinstance(player, Player)
    # Player should have typed buffer and update method
    assert hasattr(player, "typed")
    assert hasattr(player, "update")
    pygame.quit()


def test_create_zombie():
    pygame.init()
    z = EntityFactory.create_zombie()
    assert isinstance(z, Zombie)
    assert hasattr(z, "word") and isinstance(z.word, str)
    assert hasattr(z, "progress")
    assert hasattr(z, "type_char")
    pygame.quit()
