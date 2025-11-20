import pygame
from core.state import State
from entities.factory import EntityFactory
from settings import WIDTH, HEIGHT, BG_COLOR, ZOMBIE_SPAWN_INTERVAL
from states.game_over_state import GameOverState
import os

class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.factory = EntityFactory()
        self.player = self.factory.create_player()
        self.zombies = []
        self.spawn_timer = 0.0
        self.score = 0
        bg_path = "assets/field/PNG/grass.png"
        if os.path.exists(bg_path):
            try:
                raw_image = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(raw_image, (WIDTH, HEIGHT))
            except pygame.error:
                self.background = None
        else:
            self.background = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.unicode
            if key and key.isprintable():
                for z in self.zombies:
                    if not z.dying and self.player.laser_rect.colliderect(z.rect):
                        if z.word[z.progress :].startswith(key):
                            result = z.type_char(key)
                            
                            if result == "KILLED":
                                self.score += 1
                            break
                            
        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= ZOMBIE_SPAWN_INTERVAL:
            self.spawn_timer = 0.0
            self.zombies.append(self.factory.create_zombie())

        self.player.update(dt)

        for z in self.zombies[:]:
            z.update(dt)
            
            if z.is_dead():
                self.zombies.remove(z)
                continue

            if not z.dying and z.rect.x > WIDTH:
                self.game.change_state(GameOverState, score=self.score)
                return

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        self.player.draw_ui(screen)

        for z in self.zombies:
            z.draw(screen)

        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 120, 10))