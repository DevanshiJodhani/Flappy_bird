
import pygame
import time
import sys
from bird import Bird
from pipe import Pipe
pygame.init()


class Game:
    def __init__(self):

        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.window = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.move_speed = 250
        self.start_monitoring = False
        self.score = 0

        fonts = pygame.font.get_fonts()
        # for font in fonts:
        #     print(font)

        font_name = "Arial"
        font_size = 30
        self.font = pygame.font.SysFont(font_name, font_size)
        self.score_text = self.font.render(
            f"Score: {self.score}", True, (0, 0, 0))
        self.score_text_rect = self.score_text.get_rect(center=(150, 40))

        self.restart_text = self.font.render("Restart", True, (0, 0, 0))
        self.restart_text_rect = self.restart_text.get_rect(center=(300, 700))

        self.bird = Bird(self.scale_factor)
        self.is_enter_pressed = False
        self.is_game_started = True
        self.pipes = []
        self.pipe_generate_counter = 71
        self.setupBackgroundAndBase()

        #  Initialize mixer and load sounds
        pygame.mixer.init()
        self.wing_sound = pygame.mixer.Sound("./gallery/audio/wing.mp3")
        self.point_sound = pygame.mixer.Sound("./gallery/audio/point.mp3")
        self.die_sound = pygame.mixer.Sound("./gallery/audio/die.mp3")
        self.is_game_over = False

        self.gameLoop()

    def gameLoop(self):
        last_time = time.time()
        while True:
            #  calculting delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and self.is_game_started:
                    if event.key == pygame.K_RETURN:
                        self.is_enter_pressed = True
                        self.bird.update_on = True
                    if event.key == pygame.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)
                        self.wing_sound.play()
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.restart_text_rect.collidepoint(pygame.mouse.get_pos()):
                        self.restartGame()
                    

            self.updateEverything(dt)
            self.checkCollisions()
            self.checkScore()
            self.drawEverything()
            pygame.display.update()
            self.clock.tick(60)

    def restartGame(self):
        if self.is_game_started and self.bird.rect.bottom > 568:
            self.is_enter_pressed = False
            self.is_game_started = False
            if not self.is_game_over:
                self.die_sound.play()
            self.is_game_over = True
            return

        self.score = 0
        self.score_text = self.font.render(
            f"Score: {self.score}", True, (0, 0, 0))
        self.is_enter_pressed = False
        self.is_game_started = True
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter = 71
        self.bird.update_on = False
        self.is_game_over = False  # Reset the game over flag

    def checkScore(self):
        # def checkScore(self):
        if len(self.pipes) > 0:
            if (self.bird.rect.right > self.pipes[0].rect_up.left and
                    self.bird.rect.right < self.pipes[0].rect_down.right and not self.start_monitoring):
                self.start_monitoring = True
            if self.bird.rect.left > self.pipes[0].rect_up.right and self.start_monitoring:
                self.start_monitoring = False
                self.score += 1
                self.score_text = self.font.render(
                    f"Score: {self.score}", True, (0, 0, 0))
                self.score_text_rect.center = (100, 30)
                self.point_sound.play()

    def checkCollisions(self):
        if len(self.pipes):
            if self.bird.rect.bottom > 568:
                self.bird.update_on = False
                self.is_enter_pressed = False
                self.is_game_started = False
            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
               self.bird.rect.colliderect(self.pipes[0].rect_up)):
                if not self.is_game_over:
                    self.die_sound.play()
                    self.is_game_over = True
                self.is_enter_pressed = False
                self.is_game_started = False

    def updateEverything(self, dt):
        if self.is_enter_pressed:
            # moving the base
            self.base1_rect.x -= int(self.move_speed * dt)
            self.base2_rect.x -= int(self.move_speed * dt)

            if self.base1_rect.right < 0:
                self.base1_rect.x = self.base2_rect.right
            if self.base2_rect.right < 0:
                self.base2_rect.x = self.base1_rect.right

            # generating the pipes
            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0
                # print("Pipe generated")
            self.pipe_generate_counter += 1

            # moving the pipes
            for pipe in self.pipes:
                pipe.update(dt)
            # removing pipes if out of the screen
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < 0:
                    self.pipes.pop(0)
                    # print("Pipe removed")

            # moving the bird
        self.bird.update(dt)

    def drawEverything(self):
        self.window.blit(self.background_image, (0, -100))
        for pipe in self.pipes:
            pipe.drawPipe(self.window)
        self.window.blit(self.base1_image, self.base1_rect)
        self.window.blit(self.base2_image, self.base2_rect)
        self.window.blit(self.bird.image, self.bird.rect)
        score_surface = self.font.render(
            f"Score: {self.score}", True, (0, 0, 0))
        score_rect = score_surface.get_rect(center=(100, 30))
        self.window.blit(score_surface, score_rect)
        if not self.is_game_started:
            self.window.blit(self.restart_text, self.restart_text_rect)

    def setupBackgroundAndBase(self):
        # Loading images for background and base
        self.background_image = pygame.transform.scale(pygame.image.load(
            "gallery/images/background.png").convert(), (600, 1066))
        self.base1_image = pygame.transform.scale_by(pygame.image.load(
            "gallery/images/base.png").convert(), self.scale_factor)
        self.base2_image = pygame.transform.scale_by(pygame.image.load(
            "gallery/images/base.png").convert(), self.scale_factor)

        self.base1_rect = self.base1_image.get_rect()
        self.base2_rect = self.base2_image.get_rect()

        self.base1_rect.x = 0
        self.base2_rect.x = self.base1_rect.right
        self.base1_rect.y = 568
        self.base2_rect.y = 568

game = Game()




