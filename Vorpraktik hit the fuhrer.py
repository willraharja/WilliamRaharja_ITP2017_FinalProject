import pygame, random, time
from pygame.locals import *
from pygame.font import *

background_image = 'Wolfenstein.jpg'
#RGB colours combination
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
DARKGRAY    = (47, 79, 79)
BRIGHTRED   = (255, 0, 0)
RED         = (200, 0, 0)
GREEN       = (0, 200, 0)
BRIGHTGREEN = (0, 255, 0)
DARKGREEN   = (0, 155, 0)
BLUE        = (0, 0, 255)

scrWidth = 800
scrHeight = 600

screen = pygame.display.set_mode((scrWidth, scrHeight))

# ---------------------------------------------------------
class Hitler(pygame.sprite.Sprite):
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
class Gun(pygame.sprite.Sprite):

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

def center_Image(screen, im):
    x = (scrWidth - im.get_width() - 10)
    y = (scrHeight - im.get_height())
    screen.blit(im, (x, 0))

def center_Screen(screen, im):
    x = (scrWidth/2)
    y = (scrHeight/2)
    screen.blit(im, (x, y))


#-----------------------------------

#variables
pygame.init()
screen = pygame.display.set_mode([655,365])
screen.fill(BLACK)
pygame.display.set_caption("Shoot-the-Fuhrer")
background = pygame.image.load(background_image).convert()
scrWidth, scrHeight = screen.get_size()
bigFont = pygame.font.Font(None, 50)


#hide the mouse cursor


font = pygame.font.Font(None, 40)

hitSnd = pygame.mixer.Sound('Gunfire.wav')
hitSnd.set_volume(1)

# create sprites and a group
mole = Hitler()
shovel = Gun()

# game variables
score = 0
mousePos = (scrWidth/2, scrHeight/2)
DELAY = 800
clock = pygame.time.Clock()
ticker_timer = pygame.time.get_ticks()
init_time = pygame.time.get_ticks() #init_time, how long the game has run since it started


def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((scrWidth/2),(scrHeight/2))
    screen.blit(TextSurf, TextRect)

    pygame.display.update()



#Universal_Button
def button(msg,x,y,w,h,ic,ac,action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
             action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont(None, 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)


#menu UI
def introduction():

    intro = True

    while intro:

        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.fill(WHITE)
        largeText = pygame.font.Font("LemonMilk.otf",55)
        TextSurf, TextRect = text_objects("Shoot the Fuhrer", largeText)
        TextRect.center = ((scrWidth/2), (scrHeight/2))
        screen.blit(TextSurf, TextRect)

        button("GO!",100,250,100,50,GREEN,BRIGHTGREEN,main)
        button("Quit",400,250,100,50,RED,BRIGHTRED,quit)

        pygame.display.update()
        clock.tick(100)


def main():

    running = True
    global score, mousePos
    #global variable to declare mousePos inside the function
    while running:

        #hide the mouse cursor
        pygame.mouse.set_visible(False)

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

        shovel.update(pygame.mouse.get_pos())
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

        if (pygame.time.get_ticks() - init_time) >= 30000:
            temp = pygame.time.get_ticks()
            if score < 20:
                while pygame.time.get_ticks() - temp <= 5000: #wait 5000 ms == 5 sec
                    screen.fill(BLACK)
                    lose = bigFont.render("PLEASE TRY AGAIN", True, WHITE)
                    center_Screen(screen, lose)
                    pygame.display.update()
                else:
                    print("0: The Game Exit in 10, You Lost!")
                    exit()
            else:

                while pygame.time.get_ticks()-temp <= 5000: #wait 5000ms
                    screen.fill(WHITE)
                    win = bigFont.render("YOU WIN!", True, BLACK)
                    center_Screen(screen, win)
                    pygame.display.update()
                else:
                    print("0: The Game Exit in 30, You Win!")
                    exit()

# -------------------------------------------------
        # redraw game
        screen.blit(background, (0, 0))
        mole.draw(screen)
        shovel.draw(screen)

        # time elapsed (in secs)
        time = int(pygame.time.get_ticks()/1000)
        timeIm = font.render(str(time), True, WHITE)
        screen.blit(timeIm, (10,10))

        hitIm = font.render("Hits = " + str(score), True, WHITE)
        center_Image(screen, hitIm)

        pygame.display.update()
        clock.tick(80)

introduction()
pygame.quit()
quit()
