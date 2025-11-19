import pygame
from core.state import State
from settings import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR
 


class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 72)
        self.font = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from states.game_state import GameState
            self.game.change_state(GameState)
        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)
        title = self.title_font.render("TYPE OR DIE", True, TEXT_COLOR)
        help_text = self.font.render("Press ENTER to start | Type the words to kill zombies", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT // 2))
