import pygame
from core.state import State
from settings import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR
 


class GameOverState(State):
    def __init__(self, game, score=0):
        super().__init__(game)
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 24)
        self.score = score

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from states.menu_state import MenuState
            self.game.change_state(MenuState)
        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BG_COLOR)
        title = self.title_font.render("GAME OVER", True, TEXT_COLOR)
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        help_text = self.font.render("Press ENTER to return to menu", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT // 2 + 40))
