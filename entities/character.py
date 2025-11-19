import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((48, 48), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        pass
