# core/director.py
from settings import (
    INITIAL_SPAWN_INTERVAL, 
    MIN_SPAWN_INTERVAL, 
    MIN_ZOMBIE_SPEED, 
    MAX_ZOMBIE_SPEED_CAP,
    SPAWN_DECAY_RATE,
    SPEED_INCREASE_RATE
)

class AIDirector:
    def __init__(self):
        # Difficulty Parameters
        self.current_difficulty_level = 1
        self.current_spawn_interval = INITIAL_SPAWN_INTERVAL
        self.current_min_speed = MIN_ZOMBIE_SPEED
        self.current_max_speed = MIN_ZOMBIE_SPEED + 20
        # Tracking
        self.score_threshold = 25  
        self.zombies_killed = 0
        self.time_since_last_spawn = 0
    
    def update(self, dt, current_score):
        self.time_since_last_spawn += dt
        
        target_level = 1 + (current_score // self.score_threshold)
        
        if target_level > self.current_difficulty_level:
            self.increase_difficulty()
            self.current_difficulty_level = target_level

    def increase_difficulty(self):
        self.current_spawn_interval = max(
            MIN_SPAWN_INTERVAL, 
            self.current_spawn_interval - SPAWN_DECAY_RATE
        )

        self.current_max_speed = min(
            MAX_ZOMBIE_SPEED_CAP, 
            self.current_max_speed + SPEED_INCREASE_RATE
        )

        self.current_min_speed = min(
            self.current_max_speed - 10, 
            self.current_min_speed + (SPEED_INCREASE_RATE / 2)
        )
    def can_spawn(self):

        if self.time_since_last_spawn >= self.current_spawn_interval:
            self.time_since_last_spawn = 0
            return True
        return False

    def get_speed_params(self):
        return int(self.current_min_speed), int(self.current_max_speed)
