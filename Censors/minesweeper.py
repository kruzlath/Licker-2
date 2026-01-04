from globals import *

class Mine_Sweeper_Censor(Censor):
    def __init__(self,picture=default_porn_picture,pixel_size=32,mine_density=0.05):
        super().__init__(picture=picture)
        self.pixel_size=pixel_size

        pixel_count=(int(self.surface.get_width()/pixel_size),int(self.surface.get_height()/pixel_size))
        self.leftovers=(self.surface.get_width()-pixel_count[0]*pixel_size,self.surface.get_height()-pixel_count[1]*pixel_size)
        self.pixel_count=pixel_count
        self.mine_density=mine_density
        self.new_game()

        self.time_till_new_game=0
        self.game_over=False
        self.mine_icon=pygame.transform.scale(pygame.image.load("Misc/Mine.png"),(pixel_size-2,pixel_size-2))
        self.flag_icon=pygame.transform.scale(pygame.image.load("Misc/Mswp Flag.png"),(pixel_size-2,pixel_size-2))
    def new_game(self):
        pixel_count=self.pixel_count
        self.mine_map=[[random()<self.mine_density for i in range(pixel_count[0])] for i in range(pixel_count[1])]
        self.total_mines=sum([sum(self.mine_map[i]) for i in range(pixel_count[1])])
        self.mine_sum_map=[[0 for i in range(pixel_count[0])] for i in range(pixel_count[1])]
        for x in range(pixel_count[0]): 
            for x_offset in range(3):
                x_offset-=1
                if x+x_offset<0 or x+x_offset>=pixel_count[0]:
                    continue
                for y in range(pixel_count[1]):
                    for y_offset in range(3):
                        y_offset-=1
                        if y+y_offset<0 or y+y_offset>=pixel_count[1]:
                            continue
                        if self.mine_map[y+y_offset][x+x_offset]==1:
                            self.mine_sum_map[y][x]+=1
        self.reveal_map=[[0 for i in range(pixel_count[0])] for i in range(pixel_count[1])]

        #mild negative tomfoolery
        self.negative_colorkey=(253,31,62)
        self.negative=pygame.Surface(self.picture.get_size())
        self.negative_surface=pygame.Surface(self.picture.get_size())
        self.negative.fill((255,255,255))
        self.negative.blit(self.picture,(0,0),special_flags=pygame.BLEND_SUB)
        self.negative_surface.set_colorkey(self.negative_colorkey)
        self.on_top_of_negative_surface=pygame.Surface(self.picture.get_size())
        self.on_top_of_negative_surface.set_colorkey((0,0,0))
        self.revealed_squares=0
    def update(self,AEH:AllEventHandler):
        for x in range(self.pixel_count[0]):
            for y in range(self.pixel_count[1]):
                
                    
                if (x+1)*self.pixel_size>AEH.mouse_pos[0]>=x*self.pixel_size:
                    if (y+1)*self.pixel_size>AEH.mouse_pos[1]>=y*self.pixel_size:
                        if AEH.click[0]:
                            if self.reveal_map[y][x]==0:
                                self.reveal_square(x,y)
                        elif AEH.click[2]:
                            self.reveal_map[y][x]=2-self.reveal_map[y][x]
        if self.time_till_new_game>0:
            self.time_till_new_game-=AEH.delta
            if self.time_till_new_game<=0:
                self.time_till_new_game=0
                self.new_game()
                self.game_over=False
    def reveal_square(self,x,y):
        
        if self.mine_map[y][x]==1:
            self.time_till_new_game=2
            self.game_over=True
        else:
            self.revealed_squares+=1
            self.reveal_map[y][x]=1
            if self.mine_sum_map[y][x]==0:
                for x_offset in range(3):
                    x_offset-=1
                    if x+x_offset<0 or x+x_offset>=self.pixel_count[0]:
                        continue
                    for y_offset in range(3):
                        y_offset-=1
                        if y+y_offset<0 or y+y_offset>=self.pixel_count[1]:
                            continue
                        if self.reveal_map[y+y_offset][x+x_offset]==0:
                            self.reveal_square(x+x_offset,y+y_offset)
    def draw(self):
        self.negative_surface.blit(self.negative,(0,0))
        self.on_top_of_negative_surface.fill(self.negative_colorkey)
        for x in range(self.pixel_count[0]):
            for y in range(self.pixel_count[1]):
                if self.game_over==False:
                    if self.reveal_map[y][x]==0:
                        pygame.draw.rect(self.on_top_of_negative_surface,(155,155,155),(x*self.pixel_size,y*self.pixel_size,self.pixel_size,self.pixel_size))
                    elif self.reveal_map[y][x]==2:
                        self.on_top_of_negative_surface.blit(self.flag_icon,(x*self.pixel_size+1,y*self.pixel_size+1))
                    else:
                        if self.mine_sum_map[y][x]!=0:
                            center(render_text(str(self.mine_sum_map[y][x]),font="Arial",color=(0,0,0),antial=False,size=self.pixel_size),self.on_top_of_negative_surface,x*self.pixel_size+self.pixel_size/2,y*self.pixel_size+self.pixel_size/2)
                elif self.time_till_new_game>0:
                    #pygame.draw.rect(self.on_top_of_negative_surface,(155,55,55),(x*self.pixel_size,y*self.pixel_size,self.pixel_size,self.pixel_size))
                    if self.mine_map[y][x]:
                        self.on_top_of_negative_surface.blit(self.mine_icon,(x*self.pixel_size+1,y*self.pixel_size+1))
                    elif self.reveal_map[y][x]==0:
                        pygame.draw.rect(self.on_top_of_negative_surface,(155,155,155),(x*self.pixel_size,y*self.pixel_size,self.pixel_size,self.pixel_size))
                    elif self.reveal_map[y][x]==2:
                        self.on_top_of_negative_surface.blit(self.flag_icon,(x*self.pixel_size+1,y*self.pixel_size+1))
                    else:
                        if self.mine_sum_map[y][x]!=0:
                            center(render_text(str(self.mine_sum_map[y][x]),font="Arial",color=(0,0,0),antial=False,size=self.pixel_size),self.on_top_of_negative_surface,x*self.pixel_size+self.pixel_size/2,y*self.pixel_size+self.pixel_size/2)

                pygame.draw.rect(self.on_top_of_negative_surface,(55,55,55),(x*self.pixel_size,y*self.pixel_size,self.pixel_size,self.pixel_size),1)
                    
                #pygame.draw.rect(self.on_top_of_negative_surface,(0,0,0),(x*self.pixel_size,y*self.pixel_size,self.pixel_size,self.pixel_size),1,5)
        self.negative_surface.blit(self.on_top_of_negative_surface,(0,0))
        self.surface.blit(self.picture,(0,0))
        self.surface.blit(self.negative_surface,(0,0))
        pygame.draw.rect(self.surface,(55,55,55),(self.pixel_count[0]*self.pixel_size,0,self.leftovers[0],self.height))
        pygame.draw.rect(self.surface,(55,55,55),(0,self.pixel_count[1]*self.pixel_size,self.width,self.leftovers[1]))
        