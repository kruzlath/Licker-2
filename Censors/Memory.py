from globals import *
from Misc.card import *
class Memory_Censor(Censor):
    def __init__(self,picture=default_porn_picture,x_cards=7,y_cards=8):
        super().__init__(picture=picture)
        self.total_cards_revealed=0
        self.current_cards_revealed=0
        self.cards=[[Card() for i in range(x_cards)] for i in range(y_cards)]
        unused_cards=[(i%x_cards,i//x_cards) for i in range(x_cards*y_cards)]
        for i in range(int(x_cards*y_cards/2)):
            slutty_word=slutty_word_list[i]
            for i in range(2):
                this_card=choice(unused_cards)
                unused_cards.remove(this_card)
                the_card=self.cards[this_card[1]][this_card[0]]
                center(pygame.transform.rotate(render_text(slutty_word,font="Arial",color=(255,0,255),size=60),90),the_card.sides["Front"],105,160)
                the_card.word=slutty_word
                the_card.removed=False
        self.card_width=self.surface.get_width()/x_cards
        self.card_height=self.surface.get_height()/y_cards
        
        self.current_word=""
        self.x_cards=x_cards
        self.y_cards=y_cards
        self.cards_dont_match=False
        self.cards_can_be_removed=False
    def update(self,AEH:AllEventHandler):
        pass
        if AEH.click[0]:
            for x in range(self.x_cards):
                for y in range(self.y_cards):
                    if self.cards[y][x].removed:
                        continue
                    if (x+1)*self.card_width>AEH.mouse_pos[0]>=x*self.card_width and (y+1)*self.card_height>AEH.mouse_pos[1]>=y*self.card_height:
                        if self.cards[y][x].data["Side On Top"]=="Back":
                            if self.current_cards_revealed>=2:
                                break
                            self.cards_can_be_removed=False
                            self.cards_dont_match=False
                            
                            if self.current_cards_revealed==0:
                                self.current_word=self.cards[y][x].word
                            else:
                                if self.current_word!=self.cards[y][x].word:
                                    self.cards_dont_match=True
                                else:
                                    self.cards_can_be_removed=True
                            self.current_cards_revealed+=1
                            
                            self.cards[y][x].flip(30)
            y*self.card_height
        #    center(self.mask,self.map,AEH.mouse_pos[0],AEH.mouse_pos[1],pygame.BLEND_ADD)
    def draw(self):
        self.surface.blit(self.picture,(0,0))
        are_cards_flipping=False
        for x in range(self.x_cards):
            for y in range(self.y_cards):
                if self.cards[y][x].removed:
                    continue
                
                if len(self.cards[y][x].animations)>0:
                    are_cards_flipping=True
                if self.cards[y][x].cached_picture==None:
                    self.cards[y][x].cached_picture=pygame.transform.scale(pygame.transform.rotate(self.cards[y][x].sprite,-90),(self.card_width,self.card_height))
                self.surface.blit(self.cards[y][x].minimise_and_draw((self.card_width,self.card_height)),(x*self.card_width,y*self.card_height))
        if are_cards_flipping==False and self.cards_dont_match:
            for x in range(self.x_cards):
                for y in range(self.y_cards):
                    if self.cards[y][x].removed:
                        continue
                    if self.cards[y][x].data["Side On Top"]=="Front":
                        self.cards[y][x].flip(30)
            self.current_cards_revealed=0
        elif are_cards_flipping==False and self.cards_can_be_removed:
            for x in range(self.x_cards):
                for y in range(self.y_cards):
                    if self.cards[y][x].removed:
                        continue
                    if self.cards[y][x].data["Side On Top"]=="Front":
                        self.cards[y][x].removed=True
            self.current_cards_revealed=0