import random
import time
import pygame

from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS, BIRD, SCREEN_WIDTH
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

X_POS = 80
Y_POS = 310

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.typeObstacles = [SMALL_CACTUS, LARGE_CACTUS, BIRD]
        
        
    def update(self, game):
        if(game.score <= 200):
            if len(self.obstacles) == 0:
                self.append(game)
        else:
            if len(self.obstacles) <= 1:
                if len(self.obstacles) == 1:
                    if self.obstacles[0].rect.x <= SCREEN_WIDTH / 2:
                        self.append(game)
                else:
                    self.append(game)
        
        for obstacle in self.obstacles:
            if isinstance(obstacle, Bird):
                obstacle.fly()
            
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if not game.player.has_power_up:
                    death = pygame.mixer.music
                    death.load("dino_runner/assets/Songs/death.wav")
                    death.play()
                    pygame.time.delay(500)
                    game.playing = False
                    game.death_count += 1
                    game.game_speed = 20
                    game.score_actual = game.score
                    if(game.score_actual > game.max_score):
                        game.max_score = game.score_actual
                    game.score = 0
                    game.black = False
                    game.player.reset()
                    break
                else:
                    self.obstacles.remove(obstacle)
    
    def append(self, game):
        if game.score < 100:
            self.obstacles.append(Cactus(self.typeObstacles[0]))
        elif game.score < 200:
            type = random.randint(0, 1)
            self.obstacles.append(Cactus(self.typeObstacles[type]))
        else:
            type = random.randint(0, 2)
            if type < 2:
                self.obstacles.append(Cactus(self.typeObstacles[type]))
            else:
                self.obstacles.append(Bird(self.typeObstacles[type]))

    def reset_obstacles(self):
        self.obstacles = []
        
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)