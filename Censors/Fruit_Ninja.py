from globals import *

class Fruit_Censor(Censor):
    def __init__(self,picture=default_porn_picture):
        super().__init__(picture=picture)
        self.mouse_pos_memory=[]
    def update(self,AEH:AllEventHandler):
        if AEH.click[0]:
            self.mouse_pos_memory=[]
        #    center(self.mask,self.map,AEH.mouse_pos[0],AEH.mouse_pos[1],pygame.BLEND_ADD)
        if AEH.mouse_down[0]:
            dist_from_last=AEH.mouse_rel
            self.mouse_pos_memory.append((AEH.mouse_pos,atan2(AEH.mouse_rel[1],AEH.mouse_rel[0]))) #logs the distance and the angle from which the stroke came. (hehe, get it? stroke, cum :3)
            if len(self.mouse_pos_memory)==15:
                self.mouse_pos_memory.pop(0)
        else:
            if len(self.mouse_pos_memory)>0:
                self.mouse_pos_memory.pop(0)
    def draw(self):
        self.surface.blit(self.picture,(0,0))
        self.surface.blit(self.map,(0,0),special_flags=pygame.BLEND_MULT)
        if len(self.mouse_pos_memory)>0:
            positions=[]
            reverse_positions=[]
            for I,i in enumerate(self.mouse_pos_memory):
                I/=2
                positions.append((i[0][0]+cos(i[1]+pi/2)*I,i[0][1]+sin(i[1]+pi/2)*I))
                reverse_positions.append((i[0][0]-cos(i[1]+pi/2)*I,i[0][1]-sin(i[1]+pi/2)*I))
            reverse_positions.append((i[0][0]+cos(i[1])*I,i[0][1]+sin(i[1])*I))
            pygame.draw.polygon(self.surface,(255,255,255),(positions+reverse_positions[::-1]))
                
                