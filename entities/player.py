import pygame
from .character import Character
from settings import PLAYER_POS, TEXT_COLOR


class Player(Character):
    def __init__(self, pos=PLAYER_POS):
        super().__init__(pos)
        self.font = pygame.font.SysFont(None, 28)
        self.typed = ""

    def type_char(self, char):
        self.typed += char

    def clear_typed(self):
        self.typed = ""

    def draw_ui(self, surface):
        text = self.font.render(f"Typed: {self.typed}", True, TEXT_COLOR)
        surface.blit(text, (10, 10))
