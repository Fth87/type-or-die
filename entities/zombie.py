import pygame
import os
from .character import Character
from settings import TEXT_COLOR
from core.animation import load_gif_frames

class Zombie(Character):
    FRAMES = []
    FALL_IMAGE = None
    EXPLOSION_FRAMES = []
    ANIMATION_SPEED = 0.1
    SIZE = (150, 150)

    def __init__(self, pos, word, speed=60):
        super().__init__(pos)
        self.word = word
        self.speed = speed
        self.progress = 0
        self.font = pygame.font.SysFont(None, 30)
        self.dying = False
        self.death_timer = 0.0
        self.DEATH_DURATION = 1.0
        self.exact_x = float(pos[0])

        if not Zombie.FRAMES or not Zombie.FALL_IMAGE or not Zombie.EXPLOSION_FRAMES:
            self._load_assets()

        self.current_frame_index = 0
        self.animation_timer = 0.0
        self.explosion_index = 0

        if Zombie.FRAMES:
            self.image = Zombie.FRAMES[0]
            self.rect = self.image.get_rect(center=pos)
        else:
            self.image = pygame.Surface(Zombie.SIZE, pygame.SRCALPHA)
            self.image.fill((80, 180, 80))
            self.rect = self.image.get_rect(center=pos)

    def _load_assets(self):
        base_path = "assets/images/char/Zombie"
        if not Zombie.FRAMES:
            for i in range(8):
                filename = f"walk{i}.png"
                full_path = os.path.join(base_path, filename)
                if os.path.exists(full_path):
                    try:
                        img = pygame.image.load(full_path).convert_alpha()
                        img = pygame.transform.scale(img, Zombie.SIZE)
                        Zombie.FRAMES.append(img)
                    except pygame.error:
                        pass

        if not Zombie.FALL_IMAGE:
            fall_path = os.path.join(base_path, "fall.png")
            if os.path.exists(fall_path):
                try:
                    img = pygame.image.load(fall_path).convert_alpha()
                    Zombie.FALL_IMAGE = pygame.transform.scale(img, Zombie.SIZE)
                except pygame.error:
                    pass
        
        if not Zombie.EXPLOSION_FRAMES:
            Zombie.EXPLOSION_FRAMES = load_gif_frames("assets/images/fire/meledak.gif", (100, 100))

    def update(self, dt):
        if self.dying:
            self.death_timer += dt
            
            # Play explosion animation
            if Zombie.EXPLOSION_FRAMES:
                self.animation_timer += dt
                if self.animation_timer >= 0.1: # Explosion speed
                    self.animation_timer = 0
                    self.explosion_index += 1
                    if self.explosion_index < len(Zombie.EXPLOSION_FRAMES):
                        self.image = Zombie.EXPLOSION_FRAMES[self.explosion_index]
                        self.rect = self.image.get_rect(center=self.rect.center)
            return

        self.exact_x += self.speed * dt
        self.rect.x = int(self.exact_x)

        if Zombie.FRAMES:
            self.animation_timer += dt
            if self.animation_timer >= Zombie.ANIMATION_SPEED:
                self.animation_timer = 0.0
                self.current_frame_index = (self.current_frame_index + 1) % len(Zombie.FRAMES)
                self.image = Zombie.FRAMES[self.current_frame_index]

    def start_dying(self):
        self.dying = True
        self.animation_timer = 0
        self.explosion_index = 0
        if Zombie.EXPLOSION_FRAMES:
            self.image = Zombie.EXPLOSION_FRAMES[0]
            self.rect = self.image.get_rect(center=self.rect.center)
            # Adjust duration to match animation length
            self.DEATH_DURATION = len(Zombie.EXPLOSION_FRAMES) * 0.1
        elif Zombie.FALL_IMAGE:
            self.image = Zombie.FALL_IMAGE
            old_center = self.rect.center
            self.rect = self.image.get_rect(center=old_center)
            self.rect.y += 10

    def is_word_complete(self):
        return self.progress >= len(self.word)

    def is_dead(self):
        return self.dying and self.death_timer >= self.DEATH_DURATION

    def type_char(self, char):
        if self.dying:
            return False

        if self.word[self.progress] == char:
            self.progress += 1
            if self.progress >= len(self.word):
                self.start_dying()
                return "KILLED"
            return True
        return False

    def draw(self, screen):
        if self.dying:
            # No alpha fade for explosion, just draw it
            screen.blit(self.image, self.rect)
            return

        screen.blit(self.image, self.rect)
        txt = self.font.render(self.word, True, TEXT_COLOR)
        text_x = self.rect.centerx - (txt.get_width() // 2)
        text_y = self.rect.top - 25
        screen.blit(txt, (text_x, text_y))
        progress_txt = self.font.render(self.word[: self.progress], True, (255, 0, 0))
        screen.blit(progress_txt, (text_x, text_y))