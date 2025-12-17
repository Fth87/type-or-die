import pygame
from core.state import State
from entities.factory import EntityFactory
from core.director import AIDirector
from core.score_manager import ScoreManager
from settings import WIDTH, HEIGHT, BG_COLOR
from states.game_over_state import GameOverState
from entities.projectile import Projectile
import os

class GameState(State):
    """
    State utama permainan (Gameplay).
    
    Mengatur logika permainan, spawning zombie, input pemain,
    dan transisi ke Game Over.
    """
    def __init__(self, game):
        """
        Inisialisasi GameState.
        
        Menyiapkan player, factory, director, dan background.
        """
        super().__init__(game)
        self.factory = EntityFactory()
        self.player = self.factory.create_player()
        self.zombies = []
        self.projectiles = pygame.sprite.Group()
        self.spawn_timer = 0.0
        self.score = 0
        self.director = AIDirector()
        self.game_over_timer = 0.0
        self.is_game_over = False
        
        # Font UI
        self.ui_font = pygame.font.SysFont(None, 40)
        self.high_score = ScoreManager.get_best_score()

        bg_path = "assets/images/field/PNG/grass.png"
        if os.path.exists(bg_path):
            try:
                raw_image = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(raw_image, (WIDTH, HEIGHT))
            except pygame.error:
                self.background = None
        else:
            self.background = None

        self.sfx_shoot = None
        self.sfx_death = None
        try:
            shoot_path = "assets/gun-shot.wav"
            
            if os.path.exists(shoot_path):
                self.sfx_shoot = pygame.mixer.Sound(shoot_path)
                self.sfx_shoot.set_volume(0.4)
                print(f"Warning: Shoot SFX not found at {shoot_path}")
            
            death_path = "assets/death.wav"
            
            if os.path.exists(death_path):
                self.sfx_death = pygame.mixer.Sound(death_path)
                self.sfx_death.set_volume(0.8) 
            else:
                print(f"Warning: Death SFX not found at {death_path}")

        except Exception as e:
            print(f"Audio Error: {e}")

    def handle_event(self, event):
        """
        Menangani input pemain saat bermain.
        
        Mendeteksi ketikan karakter untuk menyerang zombie.
        Jika salah ketik, pemain terkena damage.
        """
        if self.is_game_over:
            return

        if event.type == pygame.KEYDOWN:
            key = event.unicode
            if key and key.isprintable():
                hit_any = False
                for z in self.zombies:
                    if not z.dying and self.player.laser_rect.colliderect(z.rect):
                        if z.word[z.progress :].startswith(key):
                            result = z.type_char(key)
                            hit_any = True
                            
                            # Spawn projectile
                            self.projectiles.add(Projectile(self.player.rect.center, z.rect.center))
                            
                            if self.sfx_shoot:
                                self.sfx_shoot.play()

                            if result == "KILLED":
                                self.score += 1
                                if self.score > self.high_score:
                                    self.high_score = self.score
                            break
                
                if not hit_any:
                    self.player.take_damage()
                    if self.player.hp <= 0:
                        if self.sfx_death:
                            self.sfx_death.play()
                        self.player.explode()
                        self.is_game_over = True
                        self.game_over_timer = 1.5
                            
        elif event.type == pygame.QUIT:
            self.game.quit()

    def update(self, dt):
        """
        Update logika permainan setiap frame.
        
        Mengupdate posisi player, zombie, proyektil, dan mengecek kondisi kalah.
        Menggunakan AIDirector untuk mengatur spawning zombie.
        """
        if self.is_game_over:
            self.player.update(dt) # Update player animation during game over
            self.game_over_timer -= dt
            if self.game_over_timer <= 0:
                self.game.change_state(GameOverState, score=self.score)
            return

        self.player.update(dt)
        
        # Check laser alignment
        is_aiming = False
        for z in self.zombies:
            if not z.dying and self.player.laser_rect.colliderect(z.rect):
                is_aiming = True
                break
        self.player.set_laser_active(is_aiming)

        self.projectiles.update(dt)
        self.director.update(dt, self.score)
        if self.director.can_spawn():
            min_s, max_s = self.director.get_speed_params()
            new_zombie = EntityFactory.create_zombie(min_s, max_s)
            self.zombies.append(new_zombie)

        for z in self.zombies[:]:
            z.update(dt)
            if z.is_dead():
                self.zombies.remove(z)
                continue
            if not z.dying and z.rect.left > WIDTH: 
                self.game.change_state(GameOverState, score=self.score)
                return

    def draw(self, screen):
        """
        Menggambar elemen permainan ke layar.
        """
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)

        self.player.draw_ui(screen)
        self.projectiles.draw(screen)

        for z in self.zombies:
            z.draw(screen)

        # Draw Score
        score_text = self.ui_font.render(f"Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topright=(WIDTH - 20, 20))
        
        # Draw High Score
        high_score_text = self.ui_font.render(f"High Score: {self.high_score}", True, (255, 215, 0))
        high_score_rect = high_score_text.get_rect(topright=(WIDTH - 20, 60))

        # Shadow for visibility
        score_shadow = self.ui_font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_shadow, (score_rect.x + 2, score_rect.y + 2))
        screen.blit(score_text, score_rect)

        high_score_shadow = self.ui_font.render(f"High Score: {self.high_score}", True, (0, 0, 0))
        screen.blit(high_score_shadow, (high_score_rect.x + 2, high_score_rect.y + 2))
        screen.blit(high_score_text, high_score_rect)