from globals import *

class Fracture_Censor(Censor):
    def __init__(self,picture=default_porn_picture,max_fractures=10):
        super().__init__(picture=picture)
        self.max_fractures=max_fractures
    def update(self,AEH:AllEventHandler):
        if AEH.click[0]:
            for i in range(randint(3,self.max_fractures)):
                length_of_line=-log(random(),1.02+i/4)*100
                angle=random()*tau
                size=randint(1,2)
                pygame.draw.polygon(self.map,(255,255,255),(
                    (AEH.mouse_pos[0]+cos(angle+pi/2)*size,AEH.mouse_pos[1]+sin(angle+pi/2)*size),
                    (AEH.mouse_pos[0]-cos(angle+pi/2)*size,AEH.mouse_pos[1]-sin(angle+pi/2)*size),
                    (AEH.mouse_pos[0]+cos(angle)*length_of_line,AEH.mouse_pos[1]+sin(angle)*length_of_line),
                ))