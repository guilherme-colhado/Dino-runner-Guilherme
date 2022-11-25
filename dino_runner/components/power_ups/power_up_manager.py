import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.time import Time

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300) 
        self.type_powers = [Shield, Hammer ,Time]

    def generate_power_up(self, score, player):
        if self.when_appears == score:
            self.when_appears += random.randint(200, 300) 
            if len(self.power_ups) == 0:
                if not player.has_power_up:
                    self.power_ups.append(random.choice(self.type_powers)())

    def update(self, game):
        self.generate_power_up(game.score, game.player)
        for power_up in self.power_ups:
            power_up.update(game.game_speed, self.power_ups)
            if game.player.dino_rect.colliderect(power_up.rect):
                if isinstance(power_up, Time):
                    game.game_speed -= 5
                else:
                    power_up.start_time = pygame.time.get_ticks()
                    game.player.has_power_up = True
                    game.player.type = power_up.type
                    game.player.power_up_time = power_up.start_time + (power_up.duration * 1000)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset_power_ups(self):
        self.power_ups = []
        self.when_appears = random.randint(200, 300)
