import pygame
import os
from core.state import State
from core.score_manager import ScoreManager
from settings import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        pygame.font.init()
        
        bg_path = "assets/field/PNG/background_menu_state.png"
        if os.path.exists(bg_path):
            try:
                raw_image = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(raw_image, (WIDTH, HEIGHT))
            except pygame.error:
                self.background = None
        else:
            self.background = None

        try:
            self.title_font = pygame.font.Font("assets/zombie.otf", 72)
            self.menu_font = pygame.font.Font("assets/font.ttf", 40)
            self.score_font = pygame.font.Font("assets/font.ttf", 30)
        except FileNotFoundError:
            self.title_font = pygame.font.SysFont(None, 72)
            self.menu_font = pygame.font.SysFont(None, 40)
            self.score_font = pygame.font.SysFont(None, 30)

        self.menu_options = ["Mulai", "Setting", "Keluar"]
        self.selected_index = 0
        self.best_score = ScoreManager.get_best_score()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                self.execute_option()
        elif event.type == pygame.QUIT:
            self.game.quit()

    def execute_option(self):
        selection = self.menu_options[self.selected_index]
        if selection == "Mulai":
            from states.game_state import GameState
            self.game.change_state(GameState)
        elif selection == "Setting":
            from states.settings_state import SettingsState
            self.game.change_state(SettingsState)
        elif selection == "Keluar":
            self.game.quit()

    def update(self, dt):
        pass

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        BLOOD_RED = (180, 0, 0)
        title_surf = self.title_font.render("TYPE OR DIE", True, BLOOD_RED)
        title_rect = title_surf.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        
        shadow_surf = self.title_font.render("TYPE OR DIE", True, (0, 0, 0))
        screen.blit(shadow_surf, (title_rect.x + 4, title_rect.y + 4))
        screen.blit(title_surf, title_rect)

        menu_start_y = HEIGHT // 2 - 20
        gap_y = 60
        last_button_y = 0

        for i, option_text in enumerate(self.menu_options):
            if i == self.selected_index:
                color = (255, 215, 0)
                prefix = "> "
            else:
                color = TEXT_COLOR
                prefix = "  "

            text_surf = self.menu_font.render(prefix + option_text, True, color)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, menu_start_y + i * gap_y))
            last_button_y = text_rect.bottom
            
            text_shadow = self.menu_font.render(prefix + option_text, True, (0, 0, 0))
            screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
            screen.blit(text_surf, text_rect)

        if self.best_score > 0:
            score_txt = f"Best Score: {self.best_score}"
            score_surf = self.score_font.render(score_txt, True, (255, 255, 255))
            score_rect = score_surf.get_rect(center=(WIDTH // 2, last_button_y + 60))
            
            bg_score = pygame.Surface((score_rect.width + 20, score_rect.height + 10))
            bg_score.fill((0, 0, 0))
            bg_score.set_alpha(150)
            screen.blit(bg_score, (score_rect.x - 10, score_rect.y - 5))
            
            screen.blit(score_surf, score_rect)