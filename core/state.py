from abc import ABC, abstractmethod


class State(ABC):
    """
    Kelas abstrak dasar untuk semua state permainan.
    
    Mendefinisikan antarmuka yang harus diimplementasikan oleh setiap state konkret
    (seperti MenuState, GameState, GameOverState).
    """
    def __init__(self, game):
        """
        Inisialisasi state.

        Args:
            game (Game): Referensi ke objek Game utama.
        """
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        """
        Menangani event Pygame tunggal.

        Args:
            event (pygame.event.Event): Event yang akan diproses.
        """

    @abstractmethod
    def update(self, dt):
        """
        Memperbarui logika state berdasarkan waktu delta.

        Args:
            dt (float): Waktu yang berlalu sejak frame terakhir dalam detik.
        """

    @abstractmethod
    def draw(self, screen):
        """
        Menggambar elemen state ke layar.

        Args:
            screen (pygame.Surface): Permukaan layar utama untuk menggambar.
        """
