import pygame
from core.state import State
from entities.factory import EntityFactory
from settings import WIDTH, HEIGHT, BG_COLOR, ZOMBIE_SPAWN_INTERVAL
from states.game_over_state import GameOverState


class GameState(State):
    def __init__(self, game):
        super().__init__(game)
        self.factory = EntityFactory()
        self.player = self.factory.create_player()
        self.zombies = []
        self.spawn_timer = 0.0
        self.score = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.unicode
            if key and key.isprintable():
                # try to apply typed char to first matching zombie
                for z in self.zombies:
                    if z.word[z.progress :].startswith(key):
                        z.type_char(key)
                        if z.is_dead():
                            self.zombies.remove(z)
                            self.score += 1
                        break
        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer >= ZOMBIE_SPAWN_INTERVAL:
            self.spawn_timer = 0.0
            self.zombies.append(self.factory.create_zombie())

        to_remove = []
        for z in self.zombies:
            z.update(dt)
            if z.rect.x > WIDTH:
                self.game.change_state(GameOverState, score=self.score)
                return

        # no collision yet; Update player (placeholder)
        self.player.update(dt)

    def draw(self, screen):
        screen.fill(BG_COLOR)
        # draw zombies
        for z in self.zombies:
            z.draw(screen)

        # draw player UI
        self.player.draw_ui(screen)

        # Score
        font = pygame.font.SysFont(None, 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH - 120, 10))
