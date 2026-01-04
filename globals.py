import pygame
from math import *
from random import *

PICTURE_WIDTH=1920
PICTURE_HEIGHT=1080

def resize_image(image):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height
    
    if PICTURE_WIDTH / PICTURE_HEIGHT > aspect_ratio:
        new_height = PICTURE_HEIGHT
        new_width = int(PICTURE_HEIGHT * aspect_ratio)
    else:
        new_width = PICTURE_WIDTH
        new_height = int(PICTURE_WIDTH / aspect_ratio)
    
    return pygame.transform.scale(image, (new_width, new_height))

default_porn_picture=pygame.image.load("Characters/Astolfo/2.png")
default_porn_picture=resize_image(default_porn_picture)

class Censor:
    def __init__(self,picture=default_porn_picture):
        self.is_complete_at=0.8 
        self.completeness=0 #When this reaches is_complete_at, the censor is completed, and the player moves onto the next level. 
        self.picture=picture
        self.map=pygame.Surface(self.picture.get_size())
        self.surface=pygame.Surface(self.picture.get_size())
    def draw(self):
        self.surface.blit(self.picture,(0,0))
        self.surface.blit(self.map,(0,0),special_flags=pygame.BLEND_MULT)
    def update(self):
        pass


class AllEventHandler:
    def __init__(self,screen_size):
        self.click=[False for i in range(3)]
        self.ctimer=[0,0,0]
        self.mouse_pos_multiplier=[1920/screen_size[0],1080/screen_size[1]]
        self.exit=False
        self.clock=pygame.time.Clock()
        self.update()
    def update(self):
        self.delta=self.clock.tick()/1000 #How many seconds have passed since last frame

        
        self.keys=pygame.key.get_pressed()
        self.mouse_down=pygame.mouse.get_pressed()
        self.ctimer=[(self.ctimer[i]+1)*self.mouse_down[i] for i in range(3)]
        self.click=[self.ctimer[i]==1 for i in range(3)]
        self.a_mouse_pos=pygame.mouse.get_pos()
        self.mouse_pos=[self.a_mouse_pos[i]*self.mouse_pos_multiplier[i] for i in range(2)]
        self.mouse_rel=pygame.mouse.get_rel()
        self.mouse_scroll=0
        self.exit=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.exit=True
            if event.type==pygame.MOUSEWHEEL:
                self.mouse_scroll=event.y
        if self.keys[27]:
            self.exit=True



def center(sprite,surface,x,y,special_flags:int=0): #Centers a sprite on specific coordinates
    surface.blit(sprite,(x-sprite.get_width()/2,y-sprite.get_height()/2),special_flags=special_flags)
fonts={}
texts={}
def render_text(text="TEXT NOT PROVIDED",size=20,color=(255,255,255),font="comicsansms",bold=False,italic=False,antial=True): #allows you to render text fast
    font_key=str(font)+str(size)
    text_key=str(font_key)+str(text)+str(color)+str(int(antial))
    if not font_key in fonts:
        try:
            fonts[font_key]=pygame.font.SysFont(font,int(size)) #Tries to load the file from the system
        except: #If that doesn't work
            try:
                fonts[font_key]=pygame.font.Font(font,int(size)) #Tries to load the font from a specified path, Don't do italic or bold unless very neccessary, bc pygame might do some strange stuff
            except:
                fonts[font_key]=pygame.font.SysFont("comicsansms",int(size))

    if not text_key in texts:
        texts[text_key]=fonts[font_key].render(str(text),antial,color)
    return texts[text_key]
class Vector_Element:
    def __init__(self,dimensions=2): #Might extend this later into higher dimensions, but, for now, there is no reason to
        self.dimensions=dimensions
        self.set_up=False
    def setup(self,x,y,rotation=0):
        self.x=x
        self.y=y
        self.rotation=rotation
        self.vectors=[]
        self.set_up=True
    def move_with_easing_motion_to(self,destination_x,destination_y, easing_rate=20,destination_rotation=0,delta=1): #Higher easing rate means slower easing
        easing_rate/=delta
        self.x=(self.x*(easing_rate-1)+destination_x)/easing_rate
        self.y=(self.y*(easing_rate-1)+destination_y)/easing_rate
        self.rotation=(self.rotation*(easing_rate-1)+destination_rotation)/easing_rate
