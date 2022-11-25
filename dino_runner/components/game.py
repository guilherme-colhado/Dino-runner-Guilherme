import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, RESTART, GAME_OVER
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.cloud import Cloud


FONT_STYLE = "dino_runner/assets/Fonts/PressStart2P-Regular.ttf"
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
        


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.running = False
        self.game_speed = 20
        self.max_score = 0
        self.score = 0
        self.black = False
        self.score_actual = 0
        self.death_count = 0
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.cloud = Cloud()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.playing = True
        self.obstacle_manager.reset_obstacles()
        self.power_up_manager.reset_power_ups()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.cloud.update(self.game_speed)
        self.update_score()

    def update_score(self):
        self.score += 1
        if self.score % 100 == 0:
            self.game_speed += 5
        if self.score % 250 == 0:
            self.black = not self.black

    def draw(self):
        self.clock.tick(FPS)
        
        if self.black:
            self.screen.fill((13, 17, 23))
        else:
            self.screen.fill((255, 255, 255)) # "FFFFFF"

        self.draw_background(True)
        self.player.draw(self.screen, self.score)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.cloud.draw(self.screen)
        self.draw_power_up_time()
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def write(self, txt, x, y):
        font = pygame.font.Font(FONT_STYLE, 22)
        text = font.render(txt, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text, text_rect)
    
    def draw_background(self, is_running):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if is_running:
            if self.x_pos_bg <= -image_width:
                self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
                self.x_pos_bg = 0
            self.x_pos_bg -= self.game_speed

    def draw_score(self):
        self.write(f"Score:{self.score}", 960, 50)
        self.write(f"Max Score:{self.max_score}", 680, 50)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_up_time - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                self.write(f"{self.player.type.capitalize()} enabled for {time_to_show} seconds", 500, 500)
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE


    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN: # não confundir com K_DOWN
                pygame.time.delay(500)
                self.run()

    def show_menu(self):
        self.screen.fill((255, 255, 255))
        self.draw_background(False)
        self.player.draw(self.screen, self.score)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        
        if self.death_count == 0:
            self.write("Press any key to start", HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT)
            self.screen.blit(ICON, (HALF_SCREEN_WIDTH - 40, HALF_SCREEN_HEIGHT - 140))
        else:
            self.screen.blit(RESTART, (HALF_SCREEN_WIDTH - 40, HALF_SCREEN_HEIGHT - 80))
            self.screen.blit(GAME_OVER, (HALF_SCREEN_WIDTH - 175, HALF_SCREEN_HEIGHT - 140))
            self.write("Press any key to restart", HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT + 150)
            self.write(f"Max Score:{self.max_score} | Score:{self.score_actual} | Deaths:{self.death_count}", HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT + 200)

        pygame.display.update()
        self.handle_events_on_menu()