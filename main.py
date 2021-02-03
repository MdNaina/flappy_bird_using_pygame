import pygame
import time
import os
import random

pygame.init()

WIN_WIDTH = 500
WIN_HEIGHT = 700
SRC_DIR = 'images'


BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join(SRC_DIR, f'bird{str(i)}.png'))) for i in range(1,4)] # looping over three images by for loop
# print(len(BIRD_IMGS))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(SRC_DIR, 'pipe.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join(SRC_DIR, 'base.png')))
BACKGROUND_IMG = pygame.transform.scale(pygame.image.load(os.path.join(SRC_DIR, 'bg.png')), (WIN_WIDTH, WIN_HEIGHT))

STAT_FONT = pygame.font.SysFont('comicsans', 40)

BIG_FONT = pygame.font.SysFont('comicsans', 80)
MEDIAM_FONT = pygame.font.SysFont('comicsans', 50)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VOL = 20 
    ANIMATION_TIME = 5 

    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]


    def jumb(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y


    def move(self):
        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2


        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y <  self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VOL


    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count > self.ANIMATION_TIME*4+1:
            self.img = self.IMGS[0]
            self.img_count = 0


        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        img_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, img_rect.topleft)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()


    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP


    def move(self):
        self.x -= self.VEL


    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG


    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH


    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH


    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))        



def draw_window(win, bird, pipes, base, score):
    win.blit(BACKGROUND_IMG, (0,0))
    bird.draw(win)
    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    text = STAT_FONT.render(f'Score : {score}', 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    pygame.display.update()


def reset():
    bird = Bird(230, 300)
    base = Base(630)
    pipes = [Pipe(550)]
    # win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    running = True
    # clock = pygame.time.Clock()
    score = 0
    game_over = False
    pause = False


def main():

    running = True
    while running:
        bird = Bird(230, 300)
        base = Base(630)
        pipes = [Pipe(550)]
        win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        clock = pygame.time.Clock()
        score = 0
        game_over = False
        pause = False 


        while not game_over:
            clock.tick(30)
            # event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False
                    pause = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # print('space is clicked')
                        bird.jumb()

            bird.move()
            rem = []
            add_pipe = False
            base.move()
            for pipe in pipes:
                if pipe.collide(bird):
                    game_over = True
                    pause = True

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()

            if add_pipe:
                score += 1
                pipes.append(Pipe(550))

            for r in rem:
                rem.remove(r)

            if bird.y + bird.img.get_height() >= 630:
                # print('you touch the base')
                game_over = True
                pause = True

            draw_window(win, bird, pipes, base, score)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    running = False
                    pause = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        reset()
                        game_over = False
                        pause = False


            text = BIG_FONT.render('Game Over', 1, (255, 0,0))
            text2 = MEDIAM_FONT.render('press Enter to play again', 1, (0,0,255))
            win.blit(text, (100, 200))
            win.blit(text2, (65, 300))
            pygame.display.update()
            

    pygame.quit()
    quit()

        


main()        




