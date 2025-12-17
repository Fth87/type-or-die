import pygame
from settings import WIDTH, HEIGHT, FPS


class Game:
    def __init__(self, initial_state_cls):
        pygame.init()
        pygame.display.set_caption("Type Or Die - Base")
        # Use FULLSCREEN and SCALED to fit the 1920x1080 game to the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        self.clock = pygame.time.Clock()
        self._running = True
        self.state = initial_state_cls(self)

    def change_state(self, state_cls, *args, **kwargs):
        self.state = state_cls(self, *args, **kwargs)

    def quit(self):
        self._running = False

    def run(self):
        while self._running:
            dt = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                self.state.handle_event(event)
            self.state.update(dt)
            self.state.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
