from globals import *

class HideRect:
    def __init__(self):
        pass
class Defragment_Censor(Censor):
    def __init__(self,picture=default_porn_picture,layers=0):
        super().__init__(picture=picture)
    def update(self,AEH:AllEventHandler):
        if AEH.click[0]:
            center(self.mask,self.map,AEH.mouse_pos[0],AEH.mouse_pos[1],pygame.BLEND_ADD)