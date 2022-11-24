import random
import pygame

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

X_POS = 80
Y_POS = 310

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.typeObstacles = [SMALL_CACTUS, LARGE_CACTUS, BIRD]
        
    def update(self, game):
        if len(self.obstacles) == 0:
            if game.score < 25:
                self.obstacles.append(Cactus(self.typeObstacles[0]))
            elif game.score < 50:
                type = random.randint(0, 1)
                self.obstacles.append(Cactus(self.typeObstacles[type]))
            else:
                type = random.randint(0, 2)
                if type < 2:
                    self.obstacles.append(Cactus(self.typeObstacles[type]))
                else:
                    self.obstacles.append(Bird(self.typeObstacles[type]))
                    
        for obstacle in self.obstacles:
            if isinstance(obstacle, Bird):
                obstacle.fly()
            
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                game.death_count += 1
                game.game_speed = 20
                game.score_actual = game.score
                if(game.score_actual > game.max_score):
                    game.max_score = game.score_actual
                game.score = 0
                game.player.dino_rect = game.player.image.get_rect()
                game.player.dino_rect.y = Y_POS
                game.player.dino_rect.x = X_POS
                break
    
    def reset_obstacles(self):
        self.obstacles = []
        
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)