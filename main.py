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
from Censors.Light_In_The_Darkness import *
from Censors.Picaso import *
from Censors.Bubble import *
from Censors.Fracture import *
from Censors.Defragment import *
from Censors.Memory import *
from Censors.Fruit_Ninja import *
from Censors.minesweeper import *
base_image=resize_image(pygame.image.load("Characters/Astolfo/7.jpg"))
censors=[Mine_Sweeper_Censor(base_image,32,0.13)]



while run:
    AEH.update()
    if AEH.exit:
        run=False
    win.fill((0,0,0))
    for i in censors:
        i.update(AEH)
        i.draw()
    win.blit(i.surface,(0,0))
    SCREEN.blit(pygame.transform.scale(win,SCREEN_SIZE),(0,0))
    pygame.display.update()
pygame.quit()