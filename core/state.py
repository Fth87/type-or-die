from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_event(self, event):
        """Handle a single pygame event"""

    @abstractmethod
    def update(self, dt):
        """Update state with delta time (seconds)"""

    @abstractmethod
    def draw(self, screen):
        """Draw the state to the screen surface"""
