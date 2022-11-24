import random

from dino_runner.components.obstacles.obstacle import Obstacle


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.y_values = [220, 270, 320]
        self.rect.y = random.choice(self.y_values)
        self.step_index = 0
    
    def fly(self):
        self.type = 0 if self.step_index < 5 else 1
        self.step_index += 1
        if self.step_index >= 10:
            self.step_index = 0