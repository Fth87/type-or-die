import pygame
from .character import Character
from settings import WIDTH, HEIGHT
from core.animation import load_gif_frames

class Player(Character):
    """
    Kelas yang merepresentasikan pemain (Player).
    
    Menangani input pergerakan, rendering karakter, sistem HP, dan animasi ledakan.
    """
    def __init__(self):
        """
        Inisialisasi pemain.
        
        Memuat aset gambar, mengatur posisi awal, sistem HP, dan laser.
        """
        super().__init__((0, 0))
        # Load image from assets
        try:
            original_image = pygame.image.load("assets/images/char/Hunter/Main.png").convert_alpha()
            self.image = pygame.transform.scale(original_image, (160, 160)) # Scale to reasonable size
        except FileNotFoundError:
            print("Warning: Player image not found. Using placeholder.")
            self.image = pygame.Surface((160, 160))
            self.image.fill((0, 100, 255))
            
        self.rect = self.image.get_rect()
        self.rect.midright = (WIDTH - 20, HEIGHT // 2)
        
        # Explosion Animation
        self.explosion_frames = load_gif_frames("assets/images/fire/meledak.gif", (150, 150))
        self.exploding = False
        self.explosion_index = 0
        self.explosion_timer = 0.0
        self.EXPLOSION_SPEED = 0.1

        # HP System
        self.hp = 3
        self.hp_images = {}
        for i in range(4):
            try:
                # Load HP images (hp0.svg to hp3.svg)
                img = pygame.image.load(f"assets/images/hp/hp{i}.svg").convert_alpha()
                self.hp_images[i] = pygame.transform.scale(img, (150, 100))
            except Exception as e:
                print(f"Warning: Could not load hp{i}.svg: {e}")

        self.speed = 300
        self.laser_thickness = 10
        self.laser_color = (0, 255, 255)
        self.laser_rect = pygame.Rect(0, 0, WIDTH, self.laser_thickness)
        
        self.font = pygame.font.SysFont(None, 28)
        self.typed = ""

    def update(self, dt):
        """
        Memperbarui status pemain setiap frame.
        
        Menangani pergerakan berdasarkan input keyboard dan animasi ledakan jika aktif.

        Args:
            dt (float): Waktu delta.
        """
        if self.exploding:
            self.explosion_timer += dt
            if self.explosion_timer >= self.EXPLOSION_SPEED:
                self.explosion_timer = 0
                self.explosion_index += 1
                if self.explosion_index < len(self.explosion_frames):
                    self.image = self.explosion_frames[self.explosion_index]
                    # Keep centered
                    self.rect = self.image.get_rect(center=self.rect.center)
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed * dt
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed * dt

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))
        
        self.laser_rect.midright = self.rect.midleft
        self.laser_rect.width = self.rect.left 
        self.laser_rect.x = 0 

    def type_char(self, char):
        """
        Menambahkan karakter ke buffer pengetikan (tidak digunakan secara aktif dalam logika saat ini).

        Args:
            char (str): Karakter yang diketik.
        """
        self.typed += char

    def clear_typed(self):
        """
        Membersihkan buffer pengetikan.
        """
        self.typed = ""

    def set_laser_active(self, active):
        """
        Mengubah warna laser berdasarkan status aktif (membidik target).

        Args:
            active (bool): True jika laser sedang membidik zombie, False jika tidak.
        """
        if active:
            self.laser_color = (255, 50, 50) # Reddish when aiming at zombie
        else:
            self.laser_color = (0, 255, 255) # Cyan default

    def take_damage(self):
        """
        Mengurangi HP pemain sebesar 1 poin.
        """
        self.hp -= 1
        if self.hp < 0:
            self.hp = 0

    def explode(self):
        """
        Memulai animasi ledakan pemain.
        """
        if not self.exploding and self.explosion_frames:
            self.exploding = True
            self.explosion_index = 0
            self.image = self.explosion_frames[0]
            self.rect = self.image.get_rect(center=self.rect.center)

    def draw_ui(self, surface):
        """
        Menggambar elemen UI pemain (laser, karakter, HP bar).

        Args:
            surface (pygame.Surface): Surface tujuan penggambaran.
        """
        if not self.exploding:
            pygame.draw.rect(surface, self.laser_color, self.laser_rect)
        
        surface.blit(self.image, self.rect)
        
        # Draw HP
        if self.hp in self.hp_images:
            surface.blit(self.hp_images[self.hp], (10, 10))