from globals import *
with open("Misc/slutty_words_list.txt","r") as f:
    slutty_word_list=f.read().split("\n")
card_transparency_overlay=pygame.Surface((210,320))
card_transparency_overlay.set_colorkey((255,255,255))
card_transparency_color=(234,23,4)
card_transparency_overlay.fill((card_transparency_color))
pygame.draw.rect(card_transparency_overlay,(255,255,255),(0,0,210,320),0,15)

card_front=pygame.Surface((210,320))
pygame.draw.rect(card_front,(255,0,255),(2,2,206,316),2,15)
class Card:
    def __init__(self): #Will be called when a new card is created
        self.sides={}

        #self.side_from_surface(pygame.Surface((210,320)),"0") #Loads in the front side
        self.side_from_surface(card_front,"Back") #Loads in the back side, which i'll change later to something more pretty
        self.side_from_surface(card_front,"Front")

        self.sprite=pygame.Surface((210,320)) #This is the main sprite in case the card is ever rendered
        self.sprite.set_colorkey(card_transparency_color)
    
        self.animations=[] #A list containing all current animations happening on the card
        
        self.parent=None
        self.data={
            #Used to determine card flipping
            "Side Order In Flipping":["Front","Back"], #Standart side order, can be changed if needed. 
            "Current Side Flipped":1,
            "Side On Top":"Back"
        }
        self.draw(init=True)
        self.active=False
        self.cached_picture=None
    def flip(self,frames=1,flip_to_side=None,flip_vertically=False):
        for i in self.animations:
            if i["Type"]=="Flipping":
                return None #Stops the code if there already exists an animation doing this
        self.animations.append({
            "Type":"Flipping", #What kind of animation is happening
            "Frames Left":frames, #The ammount of frames left before the card is fully flipped
            "Max Frames":frames,
            "Custom Flip Side":flip_to_side,
            "Vertical Flip":flip_vertically
        })
        self.active=True
    def minimise_and_draw(self,new_size):
        if self.draw():
            return self.cached_picture
        else:
            self.cached_picture=pygame.transform.scale(pygame.transform.rotate(self.sprite,-90),new_size)
            return self.cached_picture
    def draw(self,delta=1,gensmall=False,init=False): #Updates the card sprite, it is recommended this is ran every frame
        if len(self.animations)==0 and not init:
            return True
        if self.parent!=None: #Draws the cards parent first
            if self.parent.type=="Creature":
                self.parent.draw(delta)
        self.sprite.fill(card_transparency_color) 
        self.default_draw=True #Is the card rendered normally?
        for i in self.animations: #Iterates through all animations
            if i["Type"]=="Flipping": 
                self.default_draw=False #Disables normal rendering
                i["Frames Left"]-=delta
                if i["Frames Left"]>i["Max Frames"]/2:
                    size_q=sin((i["Frames Left"]/i["Max Frames"]-1/2)*pi) #Don't question it, it works and that's all that matters
                    if i["Vertical Flip"]:
                        self.sprite.blit(pygame.transform.scale(self.sides[self.data["Side On Top"]],(210,320*size_q)),(0,160*(1-size_q)))
                    else:
                        self.sprite.blit(pygame.transform.scale(self.sides[self.data["Side On Top"]],(210*size_q,320)),(105*(1-size_q),0))
                else:
                    size_q=sin((1-i["Frames Left"]/i["Max Frames"]*2)*pi/2) #Just spins the card more accuratelly, assuming it is spinning in a 3d space. (yes i made the equation up, i have no clue what it should look like)
                    if i["Custom Flip Side"]==None:
                        next_side_flipped=(self.data["Current Side Flipped"]+1)%len(self.data["Side Order In Flipping"]) #Takes the next side on order, looping around to the start if neccessary
                        side_drawn=self.sides[self.data["Side Order In Flipping"][next_side_flipped]]
                    else:
                        side_drawn=self.sides[i["Custom Flip Side"]]
                    if i["Vertical Flip"]:
                        new_size=(210,size_q*320)
                        new_pos=(0,160*(1-size_q))
                    else:
                        new_size=(210*size_q,320)
                        new_pos=(105*(1-size_q),0)
                    self.sprite.blit(pygame.transform.scale(side_drawn,new_size),new_pos) 
                if i["Frames Left"]<=0: #If the card has finished turning around, the animation is removed
                    self.animations.remove(i)
                    self.active=False
                    if i["Custom Flip Side"]==None: #Sets the side on top to be the one that was just flipped to
                        self.data["Current Side Flipped"]=(self.data["Current Side Flipped"]+1)%len(self.data["Side Order In Flipping"]) #Just copied from above
                        self.data["Side On Top"]=self.data["Side Order In Flipping"][self.data["Current Side Flipped"]]
                    else:
                        self.data["Side On Top"]=i["Custom Flip Side"]
        if self.default_draw: #renders the card normally
            self.sprite.blit(self.sides[self.data["Side On Top"]],(0,0))
        if gensmall:
            self.small_sprite=pygame.transform.scale_by(self.sprite,1/3)
        return False
    def side_from_surface(self,surface,side="Front"): #Allows you to set custom images as sides of the card.
        if not side in self.sides:
            self.sides[side]=surface.subsurface((0,0,210,320)).copy() #Crops to the top left corner
            self.sides[side].blit(card_transparency_overlay,(0,0)) #Creates several
            self.sides[side].set_colorkey(card_transparency_color)
    def iflip(self,flip_to_side=None): #Flips Instantly
        if flip_to_side==None:
            flip_to_side="Front"
        self.data["Side On Top"]=flip_to_side
    def clear_animations(self):
        self.animations=[]
