import pygame
from core.state import State
from core.score_manager import ScoreManager
from settings import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR

class GameOverState(State):
    """
    State untuk layar Game Over.
    
    Menampilkan skor akhir dan menyimpan skor jika merupakan skor tertinggi.
    Memberikan opsi untuk kembali ke menu utama.
    """
    def __init__(self, game, score=0):
        """
        Inisialisasi GameOverState.
        
        Menyimpan skor dan memanggil ScoreManager untuk menyimpan high score.
        """
        super().__init__(game)
        pygame.font.init()
        self.title_font = pygame.font.SysFont(None, 48)
        self.font = pygame.font.SysFont(None, 24)
        self.score = score
        ScoreManager.save_score(score)

    def handle_event(self, event):
        """
        Menangani input di layar Game Over.
        
        Tekan ENTER untuk kembali ke Menu Utama.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            from states.menu_state import MenuState
            self.game.change_state(MenuState)
        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        """
        Update logika Game Over (tidak ada logika khusus saat ini).
        """
        pass

    def draw(self, screen):
        """
        Menggambar layar Game Over.
        """
        screen.fill(BG_COLOR)
        title = self.title_font.render("GAME OVER", True, TEXT_COLOR)
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        help_text = self.font.render("Press ENTER to return to menu", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(help_text, (WIDTH // 2 - help_text.get_width() // 2, HEIGHT // 2 + 40))