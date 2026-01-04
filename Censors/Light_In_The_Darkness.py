from globals import *

class Light_Censor(Censor):
    def __init__(self,picture=default_porn_picture,size=46):
        super().__init__(picture=picture)
        self.mask=pygame.Surface((size+32,size+32))
        self.mask.set_colorkey((0,0,0))
        for i in range(32):
            c=i/32
            pygame.draw.circle(self.mask,(255*c,255*c,255*c),((size+32)/2,(size+32)/2),int((size+32)/2)-i)
    def update(self,AEH:AllEventHandler):
        if AEH.click[0]:
            center(self.mask,self.map,AEH.mouse_pos[0],AEH.mouse_pos[1],pygame.BLEND_ADD)