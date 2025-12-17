import pygame


class Character(pygame.sprite.Sprite):
    """
    Kelas dasar untuk semua karakter dalam permainan (Player, Zombie).
    
    Mewarisi dari pygame.sprite.Sprite.
    """
    def __init__(self, pos):
        """
        Inisialisasi karakter.

        Args:
            pos (tuple): Posisi awal (x, y) karakter.
        """
        super().__init__()
        self.image = pygame.Surface((48, 48), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        """
        Memperbarui logika karakter.

        Args:
            dt (float): Waktu delta.
        """
        pass
