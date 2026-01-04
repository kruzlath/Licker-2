from globals import *

class Picaso_Censor(Censor):
    def __init__(self,picture=default_porn_picture,size=5,color_channels=2):
        super().__init__(picture=picture)
        self.mask=pygame.Surface(self.map.get_size())
        self.size=size
        self.cc=color_channels
        #self.mask.set_colorkey((0,0,0))
        self.is_holding_down=False
    def update(self,AEH:AllEventHandler):
        if AEH.click[0]:
            self.is_holding_down=True
            self.starting_coordinates=AEH.mouse_pos
        if self.is_holding_down:
            if not AEH.mouse_down[0]:
                self.mask.fill((0,0,0))
                self.is_holding_down=False
                self.ending_coordinates=AEH.mouse_pos
                angle=atan2(self.ending_coordinates[1]-self.starting_coordinates[1],self.ending_coordinates[0]-self.starting_coordinates[0])
                if self.cc==0:
                    color=(255,255,255)
                else:
                    color=[randint(0,self.cc)*255/self.cc for i in range(3)]
                map_size_diagonal=2202.9071700822983
                starting_point=[self.starting_coordinates[0]-cos(angle)*map_size_diagonal,self.starting_coordinates[1]-sin(angle)*map_size_diagonal]
                ending_point=[self.starting_coordinates[0]+cos(angle)*map_size_diagonal,self.starting_coordinates[1]+sin(angle)*map_size_diagonal]
                pygame.draw.polygon(self.mask,color,(
                    (starting_point[0]+cos(angle+pi/2)*self.size,starting_point[1]+sin(angle+pi/2)*self.size),
                    (starting_point[0]-cos(angle+pi/2)*self.size,starting_point[1]-sin(angle+pi/2)*self.size),
                    (ending_point[0]-cos(angle+pi/2)*self.size,ending_point[1]-sin(angle+pi/2)*self.size),
                    (ending_point[0]+cos(angle+pi/2)*self.size,ending_point[1]+sin(angle+pi/2)*self.size),
                ))
                self.map.blit(self.mask,(0,0),special_flags=pygame.BLEND_ADD)
                #center(self.mask,self.map,AEH.mouse_pos[0],AEH.mouse_pos[1],pygame.BLEND_ADD)