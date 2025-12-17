import pygame
from core.state import State
from entities.factory import EntityFactory
from core.director import AIDirector
from settings import WIDTH, HEIGHT, BG_COLOR
from states.game_over_state import GameOverState
from entities.projectile import Projectile
import os

class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.factory = EntityFactory()
        self.player = self.factory.create_player()
        self.zombies = []
        self.projectiles = pygame.sprite.Group()
        self.spawn_timer = 0.0
        self.score = 0
        self.director = AIDirector()
        self.game_over_timer = 0.0
        self.is_game_over = False
        bg_path = "assets/images/field/PNG/grass.png"
        if os.path.exists(bg_path):
            try:
                raw_image = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(raw_image, (WIDTH, HEIGHT))
            except pygame.error:
                self.background = None
        else:
            self.background = None

    def handle_event(self, event):
        if self.is_game_over:
            return

        if event.type == pygame.KEYDOWN:
            key = event.unicode
            if key and key.isprintable():
                hit_any = False
                for z in self.zombies:
                    if not z.dying and self.player.laser_rect.colliderect(z.rect):
                        if z.word[z.progress :].startswith(key):
                            result = z.type_char(key)
                            hit_any = True
                            
                            # Spawn projectile
                            self.projectiles.add(Projectile(self.player.rect.center, z.rect.center))
                            
                            if result == "KILLED":
                                self.score += 1
                            break
                
                if not hit_any:
                    self.player.take_damage()
                    if self.player.hp <= 0:
                        self.player.explode()
                        self.is_game_over = True
                        self.game_over_timer = 1.5
                            
        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        if self.is_game_over:
            self.player.update(dt) # Update player animation during game over
            self.game_over_timer -= dt
            if self.game_over_timer <= 0:
                self.game.change_state(GameOverState, score=self.score)
            return

        self.player.update(dt)
        self.projectiles.update(dt)
        self.director.update(dt, self.score)
        if self.director.can_spawn():
            min_s, max_s = self.director.get_speed_params()
            new_zombie = EntityFactory.create_zombie(min_s, max_s)
            self.zombies.append(new_zombie)

        for z in self.zombies[:]:
            z.update(dt)
            if z.is_dead():
                self.zombies.remove(z)
                continue
            if not z.dying and z.rect.left > WIDTH: 
                self.game.change_state(GameOverState, score=self.score)
                return

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        self.player.draw_ui(screen)
        self.projectiles.draw(screen)

        for z in self.zombies:
            z.draw(screen)

        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 120, 10))