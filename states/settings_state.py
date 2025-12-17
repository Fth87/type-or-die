import pygame
import os
from core.state import State
from settings import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR

class SettingsState(State):
    """
    State untuk menu Pengaturan.
    
    Memungkinkan pemain mengubah volume musik, tingkat kesulitan,
    dan kembali ke menu utama.
    """
    def __init__(self, game):
        """
        Inisialisasi SettingsState.
        
        Menyiapkan opsi pengaturan (Volume, Difficulty, Back).
        """
        super().__init__(game)
        pygame.font.init()
        
        bg_path = "assets/images/field/PNG/background_menu_state.png"
        if os.path.exists(bg_path):
            try:
                raw_image = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(raw_image, (WIDTH, HEIGHT))
            except pygame.error:
                self.background = None
        else:
            self.background = None


        try:
            self.title_font = pygame.font.Font("assets/fonts/zombie.otf", 50)
            self.option_font = pygame.font.Font("assets/fonts/font.ttf", 32)
        except FileNotFoundError:
            self.title_font = pygame.font.SysFont(None, 50)
            self.option_font = pygame.font.SysFont(None, 32)

        self.hint_font = pygame.font.SysFont(None, 24)

        self.settings_data = [
            {
                "label": "Music Volume",
                "type": "slider",
                "value": 50,
                "min": 0,
                "max": 100,
                "step": 10
            },
            {
                "label": "Difficulty",
                "type": "select",
                "value": 0, # Index dari choices
                "choices": ["Easy", "Normal", "Hard", "Insane"]
            },
            {
                "label": "Back",
                "type": "button"
            }
        ]
        self.selected_index = 0

    def handle_event(self, event):
        """
        Menangani input navigasi dan perubahan nilai pengaturan.
        
        Panah Atas/Bawah: Navigasi menu.
        Panah Kiri/Kanan: Mengubah nilai (Volume/Difficulty).
        Enter: Memilih opsi (Back).
        """
        if event.type == pygame.KEYDOWN:
            current_item = self.settings_data[self.selected_index]

            # --- NAVIGASI ATAS / BAWAH ---
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.settings_data)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.settings_data)

            elif event.key == pygame.K_LEFT:
                if current_item["type"] == "slider":
                    current_item["value"] = max(current_item["min"], current_item["value"] - current_item["step"])
                elif current_item["type"] == "select":
                    n_choices = len(current_item["choices"])
                    current_item["value"] = (current_item["value"] - 1) % n_choices

            elif event.key == pygame.K_RIGHT:
                if current_item["type"] == "slider":
                    current_item["value"] = min(current_item["max"], current_item["value"] + current_item["step"])
                elif current_item["type"] == "select":
                    n_choices = len(current_item["choices"])
                    current_item["value"] = (current_item["value"] + 1) % n_choices

            elif event.key == pygame.K_RETURN:
                if current_item["label"] == "Back":
                    # Kembali ke Menu Utama
                    from states.menu_state import MenuState
                    self.game.change_state(MenuState)
                elif current_item["type"] == "button":
                    print(f"Clicked {current_item['label']}")

        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        """
        Update logika pengaturan (tidak ada logika khusus saat ini).
        """
        pass

    def draw(self, screen):
        """
        Menggambar menu pengaturan ke layar.
        """
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        title_surf = self.title_font.render("SETTINGS", True, (180, 0, 0))
        title_rect = title_surf.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title_surf, title_rect)

        start_y = 200
        gap_y = 60

        for i, item in enumerate(self.settings_data):
            color = (255, 215, 0) if i == self.selected_index else TEXT_COLOR

            if item["type"] == "slider":
                display_text = f"{item['label']}: < {item['value']} >"
            elif item["type"] == "select":
                choice_text = item["choices"][item["value"]]
                display_text = f"{item['label']}: < {choice_text} >"
            else:
                display_text = item["label"]

            prefix = "> " if i == self.selected_index else "  "
            final_text = prefix + display_text

            text_surf = self.option_font.render(final_text, True, color)
            text_rect = text_surf.get_rect(center=(WIDTH // 2, start_y + i * gap_y))
            

            shadow_surf = self.option_font.render(final_text, True, (0, 0, 0))
            screen.blit(shadow_surf, (text_rect.x + 2, text_rect.y + 2))
            
            screen.blit(text_surf, text_rect)


        hint = self.hint_font.render("Use ARROW KEYS to change values | ENTER to select", True, (200, 200, 200))
        screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 40))