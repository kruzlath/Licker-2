from globals import *

class Fruit:
    def __init__(self,parent):
        self.parent=parent
        self.x=randint(0,parent.surface.get_width()-1)
        self.y=parent.surface.get_height()
        self.yspeed=-(random()*4+1.5)
        self.type=randint(0,9)==0 #Type 0 reveals a small area. Type 1 deletes a large area from the map :3
        self.xspeed=(parent.surface.get_width()/2-self.x)/300+(random()-0.5)*2
        self.dead=False
    def move(self,AEH:AllEventHandler):
        self.x+=self.xspeed*AEH.delta*100
        self.y+=self.yspeed*AEH.delta*100
        self.yspeed+=AEH.delta**2/2*100
        if abs(self.x-self.parent.surface.get_width()/2)>self.parent.surface.get_width()/2+20+self.type*10:
            self.dead=True
        if self.yspeed>0 and self.y>self.parent.surface.get_height()+20+self.type*10:
            self.dead=True
class Particle:
    def __init__(self,parent,parent_ball):
        self.x=parent_ball.x
        self.y=parent_ball.y
        self.ttl=randint(10,randint(100,randint(100,1000)))/100
        self.max_ttl=self.ttl
        self.xspeed=randint(-30,30)/15+parent.force_sum[0]
        self.yspeed=randint(-30,30)/15+parent.force_sum[1]
        self.max_size=randint(4,8)
        self.dead=False
    def move(self,AEH:AllEventHandler):
        self.x+=self.xspeed*AEH.delta*100
        self.y+=self.yspeed*AEH.delta*100
        self.yspeed+=AEH.delta**2/2*300
        self.ttl-=AEH.delta
        self.size=self.ttl/self.max_ttl*self.max_size
        if self.ttl<=0:
            self.dead=True
class Fruit_Censor(Censor):
    def __init__(self,picture=default_porn_picture):
        super().__init__(picture=picture)
        self.mouse_pos_memory=[]
        self.fruits=[]
        self.particles=[]
    def update(self,AEH:AllEventHandler):
        if AEH.click[0]:
            self.mouse_pos_memory=[]
        if AEH.mouse_down[0]:
            self.mouse_pos_memory.append((AEH.mouse_pos,atan2(AEH.mouse_rel[1],AEH.mouse_rel[0]))) #logs the distance and the angle from which the stroke came. (hehe, get it? stroke, cum :3)
            if len(self.mouse_pos_memory)==15:
                self.mouse_pos_memory.pop(0)
        else:
            if len(self.mouse_pos_memory)>0:
                self.mouse_pos_memory.pop(0)
        if random()*AEH.delta<0.0005:
            self.fruits.append(Fruit(self))
        removed_fruits=[]
        for i in self.fruits:
            i.move(AEH)
            if dist((i.x,i.y),(AEH.mouse_pos))<20+i.type*10:
                i.dead=True
                log_vector=[log(abs(AEH.mouse_rel[i]+1.7),1.7)*((AEH.mouse_rel[i]>0)*2-1) for i in range(2)]
                self.force_sum=(log_vector[0]+i.xspeed*1.7,log_vector[1]+i.yspeed*1.7)
                for ii in range(randint(4,7)):
                    self.particles.append(Particle(self,i))
                if i.type==0:
                    pygame.draw.circle(self.map,(255,255,255),(i.x,i.y),35)
                else:
                    pygame.draw.circle(self.map,(0,0,0),(i.x,i.y),105)
            if i.dead:
                removed_fruits.append(i)
        for i in removed_fruits:
            self.fruits.remove(i)
        removed_particles=[]
        for i in self.particles:
            i.move(AEH)
            if i.dead:
                removed_particles.append(i)
            pygame.draw.circle(self.map,(255,255,255),(i.x,i.y),i.size)
        for i in removed_particles:
            self.particles.remove(i)
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
        for i in self.fruits:
            if i.type==0:
                pygame.draw.circle(self.surface,(255,255,255),(i.x,i.y),20)
            else:
                pygame.draw.circle(self.surface,(255,0,0),(i.x,i.y),30,5)
                pygame.draw.circle(self.surface,(255,0,0),(i.x,i.y),20,5)
                