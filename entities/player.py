import pygame
from .character import Character
from settings import WIDTH, HEIGHT, TEXT_COLOR

class Player(Character):
    def __init__(self):
        super().__init__((0, 0))
        # Load image from assets
        try:
            original_image = pygame.image.load("assets/images/char/Hunter/Main.png").convert_alpha()
            self.image = pygame.transform.scale(original_image, (64, 64)) # Scale to reasonable size
        except FileNotFoundError:
            print("Warning: Player image not found. Using placeholder.")
            self.image = pygame.Surface((50, 50))
            self.image.fill((0, 100, 255))
            
        self.rect = self.image.get_rect()
        self.rect.midright = (WIDTH - 20, HEIGHT // 2)
        
        self.speed = 300
        self.laser_thickness = 4
        self.laser_color = (0, 255, 255)
        self.laser_rect = pygame.Rect(0, 0, WIDTH, self.laser_thickness)
        
        self.font = pygame.font.SysFont(None, 28)
        self.typed = ""

    def update(self, dt):
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
        self.typed += char

    def clear_typed(self):
        self.typed = ""

    def draw_ui(self, surface):
        pygame.draw.rect(surface, self.laser_color, self.laser_rect)
        surface.blit(self.image, self.rect)
        
        text = self.font.render(f"Typed: {self.typed}", True, TEXT_COLOR)
        surface.blit(text, (10, 10))