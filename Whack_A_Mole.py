'''
Whack_A_Mole.py
    A Shooting Simulator with Whack-A-Mole logic
Created by Excelino.Fernando/excelincode
            & William.Raharja/wilraharja
        in 21/10/2017
Version 0.1a <21/10/2017>
    Framework and Basic Logic
'''
import pygame, random, time
from pygame.locals import *
from pygame.font import *

background_image = 'Wolfenstein.jpg'
#RGB colours combination
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (47, 79, 79)
BRIGHTRED = (255, 0, 0)
RED   = (200, 0, 0)
GREEN = (0, 200, 0)
BRIGHTGREEN = (0, 200, 0)
DARKGREEN = (0, 155, 0)
BLUE  = (0, 0, 255)

# ---------------------------------------------------------
class Mole(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("adolf.png").convert_alpha()
        self.rect = self.image.get_rect()

    # move mole to a new random location when it gets hit
    def flee(self):
        x = random.randint(0, scrWidth-1-self.rect.width)
        y = random.randint(0, scrHeight-1-self.rect.height)
        self.rect.topleft = (x,y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# ---------------------------------------------------------
class Shovel(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Animated_Pistol1.png")
        self.rect = self.image.get_rect()


    # did the shovel hit the mole?
    def hit(self, target):
        self.image = pygame.image.load("Animated_Pistol2.png")
        return self.rect.colliderect(target)

    # follows the mouse cursor
    def update(self, pt):
        self.image = pygame.image.load("Animated_Pistol1.png")
        self.rect.center = pt

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# -----------------------------------

def centerImage(screen, im):
    x = (scrWidth - im.get_width() - 10)
    y = (scrHeight - im.get_height())
    screen.blit(im, (x, 0))

# ---------- main -------------

pygame.init()
screen = pygame.display.set_mode([655,365])
screen.fill(BLACK)
pygame.display.set_caption("Pimp-my-Reich")
background = pygame.image.load(background_image).convert()
scrWidth, scrHeight = screen.get_size()


#hide the mouse cursor
pygame.mouse.set_visible(False)

font = pygame.font.Font(None, 40)

hitSnd = pygame.mixer.Sound('Gunfire.wav')
hitSnd.set_volume(1)

# create sprites and a group
mole = Mole()
shovel = Shovel()

# game variables
score = 0
mousePos = (scrWidth/2, scrHeight/2)
DELAY = 800
clock = pygame.time.Clock()
ticker_time = pygame.time.get_ticks()

#in-game concept
def main():
    running = True
    global score
    while running:
        clock.tick(40)

        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                running = True

        # update game
        shovel.update(mousePos)
        ev = pygame.event.wait()
        if ev.type == QUIT:
            pygame.quit()
            break
        elif ev.type == MOUSEBUTTONDOWN:
            if shovel.hit(mole):
                hitSnd.play()
                mole.flee()
                score += 1

                pygame.time.set_timer(USEREVENT + 1, DELAY)
            else:
                hitSnd.play()
        elif ev.type == USEREVENT + 1:
            mole.flee()


        # redraw game
        screen.blit(background, (0, 0))
        mole.draw(screen)
        shovel.draw(screen)

        # time elapsed (in secs)
        time = int(pygame.time.get_ticks()/1000)
        timeIm = font.render(str(time), True, WHITE)
        screen.blit(timeIm, (10,10))

        hitIm = font.render("Hits = " + str(score), True, WHITE)
        centerImage(screen, hitIm)

        pygame.display.update()


main()
