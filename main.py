from random import *
from math import *
import pygame
from globals import *
pygame.init()
SCREEN=pygame.display.set_mode((0,0))
SCREEN_SIZE=SCREEN.get_size()
win=pygame.Surface((1920,1080))
run=True

AEH=AllEventHandler(SCREEN_SIZE)

from Censors.Picaso import *
from Censors.Bubble import *
from Censors.Fracture import *
from Censors.Defragment import *
from Censors.Memory import *
from Censors.Fruit_Ninja import *
test_censor=Fruit_Censor(resize_image(pygame.image.load("Characters/Astolfo/4.jpg")))

while run:
    AEH.update()
    if AEH.exit:
        run=False
    win.fill((0,0,0))
    test_censor.update(AEH)
    test_censor.draw()
    win.blit(test_censor.surface,(0,0))
    SCREEN.blit(pygame.transform.scale(win,SCREEN_SIZE),(0,0))
    pygame.display.update()
pygame.quit()