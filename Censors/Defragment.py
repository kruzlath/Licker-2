from globals import *

class HideRect:
    def __init__(self,box,image,depth=0):
        avg_color=[0,0,0]
        total_pixels=0
        for x in range(box[2]):
            for y in range(box[3]):
                total_pixels+=1
                try:
                    retrieved_color=image.get_at((x,y))
                except:
                    print((x,y))
                avg_color=[avg_color[i]+retrieved_color[i] for i in range(3)]
        self.color=[avg_color[i]/total_pixels for i in range(3)]
        self.box=box
        self.surface=image
        #print(self.surface.get_size())
        self.depth=depth
class Defragment_Censor(Censor):
    def __init__(self,picture=default_porn_picture,layers=2):
        super().__init__(picture=picture)
        self.rectangles=[HideRect((0,0,self.picture.get_width(),self.picture.get_height()),self.picture)]
        self.layers=layers
    def update(self,AEH:AllEventHandler):
        if AEH.click[0]:
            removed_rects=[]
            for i in self.rectangles:
                if i.box[2]+i.box[0]>AEH.mouse_pos[0]>=i.box[0] and i.box[3]+i.box[1]>AEH.mouse_pos[1]>=i.box[1]:
                    if i.depth<self.layers:
                        self.rectangles.append(HideRect((i.box[0],i.box[1],int(i.box[2]/2),int(i.box[3]/2)),i.surface.subsurface((0,0,int(i.box[2]/2),int(i.box[3]/2))),i.depth+1))
                        self.rectangles.append(HideRect((i.box[0]+int(i.box[2]/2),i.box[1],ceil(i.box[2]/2),int(i.box[3]/2)),i.surface.subsurface((int(i.box[2]/2),0,ceil(i.box[2]/2),int(i.box[3]/2))),i.depth+1))
                        self.rectangles.append(HideRect((i.box[0]+int(i.box[2]/2),i.box[1]+int(i.box[3]/2),ceil(i.box[2]/2),ceil(i.box[3]/2)),i.surface.subsurface((int(i.box[2]/2),int(i.box[3]/2),ceil(i.box[2]/2),ceil(i.box[3]/2))),i.depth+1))
                        self.rectangles.append(HideRect((i.box[0],i.box[1]+int(i.box[3]/2),int(i.box[2]/2),ceil(i.box[3]/2)),i.surface.subsurface((0,int(i.box[3]/2),int(i.box[2]/2),ceil(i.box[3]/2))),i.depth+1))
                    removed_rects.append(i)
                    break
            for i in removed_rects:
                self.rectangles.remove(i)
            #center(self.mask,self.map,AEH.mouse_pos[0],AEH.mouse_pos[1],pygame.BLEND_ADD)
    def draw(self):
        self.surface.blit(self.picture,(0,0))
        for i in self.rectangles:
            pygame.draw.rect(self.surface,i.color,i.box)