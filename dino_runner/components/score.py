import time
import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Score(Sprite):
    def __init__(self):
        self.score = 0
        self.string_score = "000"
        self.start = time.time()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 24)
        self.letter = self.font.render(self.string_score, False, (0, 0, 0))

    def update(self):
        if time.time() - self.start >= 0.5:
            self.score += 1
            self.start = time.time()
            self.string_score = f"{self.score}"
            while len(self.string_score) < 3:
                self.string_score = "0" + self.string_score
            self.letter = self.font.render(self.string_score, False, (0, 0, 0))
        
    def draw(self, screen):
        screen.blit(self.letter, (1050, 10))