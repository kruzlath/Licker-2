from globals import *
class Bubble:
    def __init__(self,x,y,size,speed):
        self.x=x
        self.y=y
        self.size=size
        self.time_left_revealed=0
        self.angle=random()*tau
        self.xspeed=cos(self.angle)*speed*100 #Multiplied by a random number, bc why the hell not
        self.yspeed=sin(self.angle)*speed*100
        
    def move(self,AEH:AllEventHandler,bof):
        self.x+=AEH.delta*self.xspeed
        self.y+=AEH.delta*self.yspeed
        if dist((self.x,self.y),AEH.mouse_pos)<self.size and AEH.click[0]:
            self.time_left_revealed+=bof
        if self.time_left_revealed>0:
            self.time_left_revealed-=AEH.delta
class Bubble_Censor(Censor):
    def __init__(self,picture=default_porn_picture,bubble_size=50,bubble_count=100,bubble_speed=0,bubbles_on_for=60):
        super().__init__(picture=picture)
        self.bubble_size=bubble_size
        self.bubbles_on_for=bubbles_on_for
        self.bubbles=[Bubble(randint(bubble_size,self.surface.get_width()-bubble_size),randint(bubble_size,self.surface.get_height()-bubble_size),bubble_size,bubble_speed) for i in range(bubble_count)]
    def update(self,AEH:AllEventHandler):
        self.map.fill((0,0,0))
        for i in self.bubbles:
            i.move(AEH,self.bubbles_on_for)
            while i.x>self.surface.get_width()+self.bubble_size:
                i.x-=self.surface.get_width()+self.bubble_size*2
            while i.x<-self.bubble_size:
                i.x+=self.surface.get_width()+self.bubble_size*2
            
            while i.y>self.surface.get_height()+self.bubble_size:
                i.y-=self.surface.get_height()+self.bubble_size*2
            while i.y<-self.bubble_size:
                i.y+=self.surface.get_height()+self.bubble_size*2
            
            if i.time_left_revealed>0:
                pygame.draw.circle(self.map,(255,255,255),(i.x,i.y),i.size)
            else:
                pygame.draw.circle(self.map,(255,255,255),(i.x,i.y),i.size,1)