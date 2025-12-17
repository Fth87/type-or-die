import pygame
import math
from core.animation import load_gif_frames

class Projectile(pygame.sprite.Sprite):
    """
    Kelas yang merepresentasikan proyektil (peluru) yang ditembakkan pemain.
    
    Menangani pergerakan peluru menuju target dan animasi rotasi.
    """
    FRAMES = []

    def __init__(self, start_pos, target_pos, speed=2500):
        """
        Inisialisasi proyektil.

        Args:
            start_pos (tuple): Posisi awal peluru.
            target_pos (tuple): Posisi target (zombie).
            speed (int): Kecepatan peluru.
        """
        super().__init__()
        if not Projectile.FRAMES:
            # Load frames once
            Projectile.FRAMES = load_gif_frames("assets/images/fire/peluru.gif", (100, 100))
        
        self.frames = Projectile.FRAMES
        self.image = self.frames[0] if self.frames else pygame.Surface((10, 10))
        self.rect = self.image.get_rect(center=start_pos)
        
        self.pos = pygame.math.Vector2(start_pos)
        self.target = pygame.math.Vector2(target_pos)
        self.speed = speed
        
        direction = self.target - self.pos
        if direction.length() > 0:
            self.velocity = direction.normalize() * self.speed
        else:
            self.velocity = pygame.math.Vector2(-1, 0) * self.speed
            
        self.animation_index = 0
        self.animation_timer = 0.0
        self.ANIMATION_SPEED = 0.05
        
        # Calculate angle
        # The sprite faces UP by default. We need to correct this.
        # atan2 returns angle from X axis (Right).
        # We subtract 90 degrees to align UP-facing sprite to the calculated angle.
        self.angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
        
        # Rotate initial image
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt):
        """
        Memperbarui posisi dan animasi peluru.

        Args:
            dt (float): Waktu delta.
        """
        self.pos += self.velocity * dt
        self.rect.center = self.pos
        
        # Animation
        if self.frames:
            self.animation_timer += dt
            if self.animation_timer >= self.ANIMATION_SPEED:
                self.animation_timer = 0
                self.animation_index = (self.animation_index + 1) % len(self.frames)
                
                # Get frame and rotate
                base_image = self.frames[self.animation_index]
                self.image = pygame.transform.rotate(base_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)

        # Kill if reached target
        if self.pos.distance_to(self.target) < 20:
            self.kill()
