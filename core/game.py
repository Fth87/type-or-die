import pygame
import sys
from settings import WIDTH, HEIGHT, FPS


class Game:
    """
    Kelas utama yang mengelola siklus hidup permainan (game loop).
    
    Kelas ini bertanggung jawab untuk inisialisasi Pygame, manajemen layar,
    pengaturan waktu (clock), dan transisi antar state permainan.
    """
    def __init__(self, initial_state_cls):
        """
        Inisialisasi instance Game.

        Args:
            initial_state_cls (class): Kelas state awal yang akan dimuat saat game dimulai.
        """
        pygame.init()
        pygame.display.set_caption("Type Or Die - Base")
        # Use FULLSCREEN and SCALED to fit the 1920x1080 game to the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        self.clock = pygame.time.Clock()
        self._running = True
        self.state = initial_state_cls(self)

    def change_state(self, state_cls, *args, **kwargs):
        """
        Mengganti state permainan saat ini ke state baru.

        Args:
            state_cls (class): Kelas state baru yang akan diinstansiasi.
            *args: Argumen posisi untuk konstruktor state baru.
            **kwargs: Argumen kata kunci untuk konstruktor state baru.
        """
        self.state = state_cls(self, *args, **kwargs)

    def quit(self):
        """
        Menghentikan loop permainan dan keluar dari aplikasi.
        """
        self._running = False

    def run(self):
        """
        Menjalankan loop utama permainan.
        
        Loop ini menangani event, pembaruan logika (update), dan penggambaran (draw)
        pada setiap frame hingga permainan dihentikan.
        """
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
        sys.exit()
