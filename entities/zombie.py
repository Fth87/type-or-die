import random
import pygame
from .character import Character
from settings import TEXT_COLOR


class Zombie(Character):
    def __init__(self, pos, word, speed=60):
        super().__init__(pos)
        self.word = word
        self.speed = speed
        self.progress = 0
        self.font = pygame.font.SysFont(None, 30)
        self.image.fill((80, 180, 80))

    def update(self, dt):
        self.rect.x += int(self.speed * dt)

    def is_dead(self):
        return self.progress >= len(self.word)

    def type_char(self, char):
        # check next char in word
        if self.word[self.progress] == char:
            self.progress += 1
            return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        txt = self.font.render(self.word, True, TEXT_COLOR)
        screen.blit(txt, (self.rect.x + 6, self.rect.y + 6))
        # draw progress underline
        progress_txt = self.font.render(self.word[: self.progress], True, (100, 255, 100))
        screen.blit(progress_txt, (self.rect.x + 6, self.rect.y + 30))
