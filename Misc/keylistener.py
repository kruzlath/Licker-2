import pygame
class Listener:
    def __init__(self):
        self.result=""
        self.listening_to=[
            pygame.K_a,
            pygame.K_b,
            pygame.K_c,
            pygame.K_d,
            pygame.K_e,
            pygame.K_f,
            pygame.K_g,
            pygame.K_h,
            pygame.K_i,
            pygame.K_j,
            pygame.K_k,
            pygame.K_l,
            pygame.K_m,
            pygame.K_n,
            pygame.K_o,
            pygame.K_p,
            pygame.K_q,
            pygame.K_r,
            pygame.K_s,
            pygame.K_t,
            pygame.K_u,
            pygame.K_v,
            pygame.K_w,
            pygame.K_x,
            pygame.K_y,
            pygame.K_z,
            pygame.K_1,
            pygame.K_2,
            pygame.K_3,
            pygame.K_4,
            pygame.K_5,
            pygame.K_6,
            pygame.K_7,
            pygame.K_8,
            pygame.K_9,
            pygame.K_0,
            pygame.K_SPACE,
            pygame.K_BACKSPACE,
            pygame.K_RETURN,
	    pygame.K_PERIOD,
	    pygame.K_MINUS,
        ]
        self.listening_keys=[[i,pygame.key.name(i),0,False,0] for i in self.listening_to]
    def update(self,key_input,delta_time=1):
        for i in self.listening_keys:
            i[2]=key_input[i[0]]*(i[2]+1)  
            i[4]=key_input[i[0]]*(i[4]+delta_time)
            i[3]=i[2]==1
            if i[3] or i[4]>=40:
                if i[0]==pygame.K_SPACE:
                    self.result+=" "
                elif i[0]==pygame.K_BACKSPACE:
                    self.result=self.result[:-1]
                elif i[0]==pygame.K_RETURN:
                    self.result+="\n"
                else:
                    if key_input[pygame.K_LSHIFT] or key_input[pygame.K_RSHIFT]:
                        if i[1] in "1234567890.-":
                            self.result+="!@#$%^&*()>_"["1234567890.-".index(i[1])]
                        else:
                            self.result+=i[1].upper()
                    else:
                        self.result+=i[1]