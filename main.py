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
test_censor=Picaso_Censor(size=4,color_channels=0)

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