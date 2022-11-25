import time
import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, HAMMER_TYPE, DUCKING_HAMMER, JUMPING_HAMMER, RUNNING_HAMMER, HEART

X_POS = 80
Y_POS = 310
JUMP_AND_DUCK_VEL = 8.5
Y_POS_DUCK = 344

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

class Dinosaur(Sprite):
    def __init__(self):
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index = 0
        self.dino_run = True
        self.dino_duck = False
        self.dino_jump = False
        self.lives = 3
        self.jump_duck_vel = JUMP_AND_DUCK_VEL
        self.setup_state()
        self.sound = pygame.mixer.music
    
    def setup_state(self):
        self.has_power_up = False
        self.power_time = 0
    
    def update(self,user_input):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.dino_duck:
            self.duck()
            
        if (user_input[pygame.K_UP] or user_input[pygame.K_SPACE]) and not self.dino_jump:
            self.sound.load("dino_runner/assets/Songs/jump.wav")
            self.sound.play()
            self.dino_jump = True
            self.dino_run = False
        elif not self.dino_jump and not self.dino_duck: 
            self.dino_run = True
    
        if user_input[pygame.K_DOWN]:
            self.dino_duck = True
        else:
            self.dino_duck = False
        
        if self.step_index > 10:
            self.step_index = 0     
    
    def run(self):
        self.image = RUN_IMG[self.type][0] if self.step_index < 5 else RUN_IMG[self.type][1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
        self.step_index += 1
    
    def jump(self):
        self.image = JUMP_IMG[self.type]
        
        if self.dino_jump and not self.dino_duck:
            self.dino_rect.y -= self.jump_duck_vel * 4
            self.jump_duck_vel -= 0.8
            
        if self.jump_duck_vel < -JUMP_AND_DUCK_VEL:
            self.dino_rect.y = Y_POS
            self.dino_jump = False
            self.jump_duck_vel = JUMP_AND_DUCK_VEL
    
    def reset(self):
        self.dino_duck = False
        self.dino_jump = False
        self.dino_run = True
        self.jump_duck_vel = JUMP_AND_DUCK_VEL
        
    
    def normal_player(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = X_POS
        self.dino_rect.y = Y_POS
    
    def duck(self):
        self.image = DUCK_IMG[self.type][0] if self.step_index < 5 else DUCK_IMG[self.type][1]
        self.step_index += 1
        if self.dino_jump and self.dino_rect.y < Y_POS_DUCK:
            self.dino_rect.y -= self.jump_duck_vel * 4
            self.jump_duck_vel -= 1.2
        else:
            self.dino_rect.y = Y_POS_DUCK
            self.jump_duck_vel = JUMP_AND_DUCK_VEL
            self.dino_jump = False
    
    def draw(self, screen, score):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
        heart = HEART
        heart_rect = heart.get_rect()
        heart_rect.x = 20
        heart_rect.y = 550
        increment = 0
        for i in range(self.lives):
            screen.blit(heart, (heart_rect.x + increment, heart_rect.y))
            increment += 30