from pygame.sprite import Sprite

from dino_runner.utils.constants import SCREEN_WIDTH, CLOUD


class Cloud(Sprite):
    def __init__(self):
        self.image = CLOUD
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + 500
        self.rect.y = 100
        
    def update(self, game_speed):
        self.rect.x -= game_speed  
        
        if self.rect.x < self.rect.width * -2:
            self.rect.x = SCREEN_WIDTH + 500
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))