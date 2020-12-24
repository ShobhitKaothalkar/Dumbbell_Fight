import pygame
from math import cos, sin, tan, pi
import sys
import os

# Music
# Breakfast on the Dark Side of the Moon by Mana Junkie (c) copyright 2020 Licensed under a Creative Commons Attribution Noncommercial  (3.0) license. http://dig.ccmixter.org/files/mana_junkie/62733 Ft: gurdonark


#os.environ['SDL_VIDEO_CENTERED'] = '1' # You have to call this before pygame.init()

pygame.init()
impact_sound = pygame.mixer.Sound("impact.wav")
ta_da = pygame.mixer.Sound("ta_da.wav")


white = (255,255,255)
peach = (255, 230, 153)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,200)

yellow = (200,200,0)
light_yellow = (255,255,0)


smallfont = pygame.font.Font("BlackRocker.ttf", 20)
medfont = pygame.font.Font("BlackRocker.ttf", 50)
largefont = pygame.font.Font("BlackRocker.ttf", 70)



# info = pygame.display.Info() # You have to call this before pygame.display.set_mode()
# display_width,display_height = info.current_w,info.current_h



display_width = 1280
display_height = 720

pen_height = 100
pointer_size = 15

FPS = 150

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.update()



# gameDisplay = pygame.display.set_mode((display_width,display_height))
# gameDisplay = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Dumbbell Fight')

pygame.mixer.get_init()

dumbbell_img_blue = pygame.image.load("dumbbell_blue.png").convert_alpha()
dumbbell_img_green = pygame.image.load("dumbbell_green.png").convert_alpha()
pointer_green_img = pygame.image.load("pointer_green.png")
pointer_red_img = pygame.image.load("pointer_red.png")
reference_img = pygame.image.load("reference.png")
star_img = pygame.image.load("star.png")

clock = pygame.time.Clock()


def message_to_screen(msg, color, y_displace = 0, size = "small"):
    if size == "small":
        textSurf = smallfont.render(msg, True, color)
    elif size == "medium":
        textSurf = medfont.render(msg, True, color)
    elif size == "large":
        textSurf = largefont.render(msg, True, color)    
    textRect = textSurf.get_rect()
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2,display_height/2])
    textRect.center = (display_width/2, display_height/2 + y_displace)
    gameDisplay.blit(textSurf, textRect)





def draw_sprites(sprites):
    gameDisplay.fill(peach)


    pygame.draw.line(gameDisplay, black, (display_width*0.22,display_height*0.2),(display_width*0.22,display_height*0.8),7)
    pygame.draw.line(gameDisplay, black, (display_width*0.78,display_height*0.2),(display_width*0.78,display_height*0.8),7)
    pygame.draw.line(gameDisplay, black, (display_width*0.22,display_height*0.2), (display_width*0.78,display_height*0.2),7)
    pygame.draw.line(gameDisplay, black, (display_width*0.22,display_height*0.8), (display_width*0.78,display_height*0.8),7)

    for sprite in sprites:
        sprite.draw()
    # pygame.draw.rect(gameDisplay, green, (0,0,display_width+85,display_height+45))
    pygame.display.update()
    clock.tick(FPS)
    
    

    # pygame.draw.line(gameDisplay, green,  (0, pen2.y + m*pen2.x),(pen2.y/m+pen2.x, 0), 5)

    

def collision_area(pen1, pen2):
    mask1 = pen1.mask
    mask2 = pen2.mask
    offset = (pen2.rect.topleft[0]-pen1.rect.topleft[0], pen2.rect.topleft[1]-pen1.rect.topleft[1])
    collide = mask1.overlap_area(mask2, offset)

    return collide

def collision(pen1, pen2):
    mask1 = pen1.mask
    mask2 = pen2.mask
    offset = (pen2.rect.topleft[0]-pen1.rect.topleft[0], pen2.rect.topleft[1]-pen1.rect.topleft[1])
    collide = mask1.overlap(mask2, offset)
    
    return collide


def calc_vel_omega(pen, dist_from_cm, force):
    # torque = dist_from_cm*force
    # alpha = (torque/(pen.mass*pen.length**2))*50
    # omega = alpha
    # acc = force/pen.mass
    # velocity = acc/FPS*7


    torque = dist_from_cm*force
    alpha = (torque/(pen.mass*pen.length**2))*15       
    omega = alpha*(abs((dist_from_cm)**3)/1000)/70    
    # self.angle = 0
    acc = force/pen.mass
    velocity = acc/12

    return velocity, omega


def calc_direction(pen, pen_collide_x, pen_collide_y ,pen2):
    # print(pen2.angle)
    if pen2.angle >= 360:
        pen2.angle = pen2.angle%360
    elif pen2.angle < 0:
        pen2.angle = pen2.angle%-360 
        pen2.angle = 360 + pen2.angle
    
    # if pen2.angle == 90:
    #     m = 0.00000001
    # elif pen2.angle == 0:
    #     m =  99999999
    # else:
    #     m = tan(1.57 - pen2.angle*(3.14/180))

    # print("Angle", pen2.angle)
    # print(m)

    x = pen_collide_x
    y = -pen_collide_y

    # axis = (y-pen2.y) - m*(x - pen2.x)
    # normal = (y-pen2.y) + 1/m*(x - pen2.x)
    axis, normal, m = 0, 0, 0

 
    x1 = pen2.x
    y1 = -pen2.y
    # print(pen2.x, pen2.y)
    # print(pen_collide_x, pen_collide_y)

    m = tan(1.57 - pen2.angle*(3.14/180))
    axis = (y-y1) - m*(x - x1)
    normal = (y-y1) + 1/m*(x - x1)
    
    
    direction = "LEFT"
    omega = "+"
    if 0 < pen2.angle < 90 :
        if axis >=  0:
            direction =  "LEFT"
            if normal >= 0:
                omega = "+"
            else:
                omega = "-"
        else:
            direction = "RIGHT"
            if normal >= 0:
                omega = "-"
            else:
                omega = "+"
    elif 90 < pen2.angle < 180:
        if axis >=  0:
            direction =  "LEFT"
            if normal >= 0:
                omega = "-"
            else:
                omega = "+"
        else:
            direction = "RIGHT"
            if normal >= 0:
                omega = "+"
            else:
                omega = "-"
    elif 180 < pen2.angle < 270:
        if axis >=  0:
            direction =  "RIGHT"
            if normal >= 0:
                omega = "+"
            else:
                omega = "-"
        else:
            direction = "LEFT"
            if normal >= 0:
                omega = "-"
            else:
                omega = "+"
    elif 270 < pen2.angle < 360:
        if axis >=  0:
            direction =  "RIGHT"
            if normal >= 0:
                omega = "-"
            else:
                omega = "+"
        else:
            direction = "LEFT"
            if normal >= 0:
                omega = "+"
            else:
                omega = "-"
    elif pen2.angle == 0 :
        if pen_collide_x < pen2.x :
            direction =  "LEFT"
            if -pen_collide_y >= pen2.y:
                omega = "+"
            else:
                omega = "-"
        elif pen_collide_x > pen2.x :
            direction =  "RIGHT"
            if -pen_collide_y >= pen2.y:
                omega = "-"
            else:
                omega = "+"
    elif pen2.angle == 180:
        if pen_collide_x < pen2.x :
            direction =  "RIGHT"
            if -pen_collide_y >= pen2.y:
                omega = "+"
            else:
                omega = "-"
        elif pen_collide_x > pen2.x :
            direction =  "LEFT"
            if -pen_collide_y >= pen2.y:
                omega = "-"
            else:
                omega = "+"

    elif pen2.angle == 90 :
        if  -pen_collide_y > pen2.y:
            direction =  "LEFT"
            if pen_collide_x <= pen2.x:
                omega = "-"
            else:
                omega = "+"
        elif  -pen_collide_y < pen2.y:
            direction =  "RIGHT"
            if pen_collide_x <= pen2.x:
                omega = "+"
            else:
                omega = "-"
    elif  pen2.angle == 270:
        if  -pen_collide_y > pen2.y:
            direction =  "RIGHT"
            if pen_collide_x <= pen2.x:
                omega = "-"
            else:
                omega = "+"
        elif  -pen_collide_y < pen2.y:
            direction =  "LEFT"
            if pen_collide_x <= pen2.x:
                omega = "+"
            else:
                omega = "-"

    
    
    # print(axis)
    # print((-pen2.y) - m*(-pen2.x))
    # print(m)
        
    return direction, omega



def move(pen, pen2, velocity, omega, direction, sprites):

    while velocity > 0 :

        if pen.angle >= 360:
            pen.angle = pen.angle%360
        elif pen.angle < 0:
            pen.angle = pen.angle%-360 
            pen.angle = 360 + pen.angle

        collide = collision_area(pen, pen2)
        if collide == 0:

            if direction == "LEFT":
                pen.angle += omega
                pen.x += velocity*cos(pen.angle*(3.14/180))
                pen.y += velocity*sin(pen.angle*(3.14/180))
            elif direction == "RIGHT":
                pen.angle -= omega
                pen.x -= velocity*cos(pen.angle*(3.14/180))
                pen.y -= velocity*sin(pen.angle*(3.14/180))            

            
            if collision(pen, pen2) != None:
                pen.x -= velocity*cos(pen.angle*(3.14/180))*2
                pen.y -= velocity*sin(pen.angle*(3.14/180))*2
                # print("BACKOFF")
                velocity = 0

            velocity -= 0.7
        else:
            pygame.mixer.Sound.play(impact_sound)
            if direction == "LEFT":
                pen.angle -= omega
                pen.x -= velocity*cos(pen2.angle*(3.14/180))
                pen.y -= velocity*sin(pen2.angle*(3.14/180))
            elif direction == "RIGHT":
                pen.angle += omega
                pen.x += velocity*cos(pen2.angle*(3.14/180))
                pen.y += velocity*sin(pen2.angle*(3.14/180))
                
            # draw_sprites(sprites)
            # print("Area", collision_area(pen, pen2))
            collide = collision(pen, pen2)
            
            # clock.tick(FPS/2)
            # draw_sprites(sprites)
                
            velocity1 = velocity
            velocity = 0
            
            pen_collide_x = collide[0]+pen.rect.topleft[0]
            pen_collide_y = collide[1]+pen.rect.topleft[1]
            
            direction, omega_dir = calc_direction(pen, pen_collide_x, pen_collide_y, pen2)
            
            if omega_dir == "-":
                omega = -omega
            
            # print(direction, omega_dir)
            # a = 0 
            # velocity1 = velocity
            
            v = 100
            while collision_area(pen, pen2) !=  0:
                
                # print(collision_area(pen1, pen2))
                # print(a)
                if pen2.angle >= 360:
                    pen2.angle = pen.angle%360
                elif pen2.angle < 0:
                    pen2.angle = pen2.angle%-360 
                    pen2.angle = 360 + pen2.angle

                if omega_dir == "-":
                    omega = -omega
                # print(direction, omega_dir)
                # half_angle = pen2.angle
                # if pen2.angle >= 180:
                #     half_angle = pen2.angle - 180
                # print(pen2.angle)


                if direction == "LEFT":
                  
                    pen2.angle += omega
                    pen2.x += v*cos(pen2.angle*(3.14/180))
                    pen2.y += v*sin(pen2.angle*(3.14/180))
                
                elif direction == "RIGHT":
                    
                    pen2.angle += omega
                    pen2.x -= v*cos(pen2.angle*(3.14/180))
                    pen2.y -= v*sin(pen2.angle*(3.14/180))

                # direction = calc_direction(pen_collide_x)
                clock.tick(FPS)

                draw_sprites(sprites)
                pygame.draw.circle(gameDisplay, black, (pen_collide_x, pen_collide_y), 5)
                pygame.display.update()

                # velocity -= 5
                # a += 1
            
            
            move(pen2, pen, velocity1, omega, direction, sprites)
        
            
        clock.tick(FPS)
        draw_sprites(sprites)
        

        

# class pointer:
#     def draw(self, pen, dist_from_cm):
#         corners = [pen.point1, pen.point2, pen.point3, pen.point4]
#         dist_from_top = pen.length/2 - dist_from_cm
#         angle = 1.57 -  pen.angle
#         x = dist_from_top*cos(angle) + corners[2][0] 
#         y = dist_from_top*sin(angle) + corners[2][1] 
#         # rotated_image = pygame.transform.rotate(pointer_green_img, 6.28 - pen.angle)
#         # gameDisplay.blit(rotated_image, (x, y))
#         pygame.draw.circle(gameDisplay, green, (x, y), 4)
#         pygame.display.update()


class score_board:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.round  = 1
        self.img = star_img


    def draw(self):
        pos1  = [display_width*0.12, display_height*0.05]
        pos2  = [display_width*0.88-20, display_height*0.05]
        
        for i in range(self.score1):
            gameDisplay.blit(self.img, pos1)
            pos1[0] += 25

        for i in range(self.score2):
            gameDisplay.blit(self.img, pos2)
            pos2[0] -= 25




class power_meter:
    def __init__(self, position, power):
        self.position = position
        self.power = power


    def draw(self):
        color = [0, 220, 0]
        power = self.power
        bars_no = int(power/5)
        x = self.position[0]
        y = self.position[1]
        for i in range(bars_no):
            pygame.draw.rect(gameDisplay, color, (x, y, 50, 10))
            color[0] += 20
            color[1] -= 20
            y -= 10
            # print(color)
            # print(i)




class pointer:
    def __init__(self, line_start, line_end):
        self.direction = "LEFT"
        self.start = line_start
        self.pos = list(line_start)
        self.end = line_end
        self.left_img = pointer_green_img
        self.right_img = pointer_red_img
        self.reference = reference_img
        self.dist_from_cm = pen_height*(self.pos[1]-line_start[1])/(line_start[1]-line_end[1]) + (pen_height/2)

    def draw(self):
        # pygame.draw.line(gameDisplay, black, self.start, self.end, 5)
        gameDisplay.blit(self.reference, self.start)
        if self.direction == "LEFT":
            gameDisplay.blit(self.left_img, (self.pos[0]-20,self.pos[1]))
        elif self.direction == "RIGHT":
            gameDisplay.blit(self.right_img, (self.pos[0]+45,self.pos[1]))

        self.dist_from_cm = pen_height*(self.pos[1]-self.start[1])/(self.start[1]-self.end[1]) + (pen_height/2)





class pen:

    def __init__(self, x, y, angle, color):
        self.x = x
        self.y = y
        self.r = 100.125
        self.theta = 1.59
        self.length = 2*(self.r*sin(self.theta))
        self.angle = angle
        self.t = 5
        if color == "blue":
            self.img = dumbbell_img_blue
        elif color == "green":
            self.img = dumbbell_img_green
        self.mass = 0.2
        self.mask = pygame.mask.from_surface(self.img)

    
    def draw(self):
    
        y = self.y
        m = tan(self.angle*(3.14/180))
        theta = self.theta
        # print(self.angle)
        t = self.t

        angle_rad = self.angle*(3.14/180)

        self.point1 = ( (self.x+self.r*cos(angle_rad+3.14-theta) ), (self.y+self.r*sin(angle_rad+3.14-theta) ) )
        self.point2 = ( (self.x+self.r*cos(angle_rad+theta) ), (self.y+self.r*sin(angle_rad+theta) ) )
        self.point3 = ( (self.x+self.r*cos(angle_rad+6.28-theta) ), (self.y+self.r*sin(angle_rad+6.28-theta) ) )
        self.point4 = ( (self.x+self.r*cos(angle_rad+3.14+theta) ), (self.y+self.r*sin(angle_rad+3.14+theta) ) )     

       

        rotated_image = pygame.transform.rotate(self.img, 360-self.angle)
        new_rect = rotated_image.get_rect(center = (self.x, self.y))
        self.rect = new_rect
        gameDisplay.blit(rotated_image, new_rect.topleft)
        # self.img = rotated_image
        self.mask = pygame.mask.from_surface(rotated_image)

        # pygame.draw.polygon(gameDisplay, red, [ self.point1, self.point2, self.point3, self.point4])
        # pygame.draw.circle(gameDisplay, black, (self.point4), 2)
        # pygame.draw.circle(gameDisplay, blue, (self.point1), 2)
        
    


# pen1 = pen(display_width*0.2, display_height*0.5, 0)
# pen2 = pen(display_width*0.8, display_height*0.5, 0)
# pointer1 = pointer((display_width*0.05,display_height*0.5-pen_height),(display_width*0.05,display_height*0.5-pen_height+150))
# pointer2 = pointer((display_width*0.95-50,display_height*0.5-pen_height),(display_width*0.95-50,display_height*0.5-pen_height+150))
# power_meter1 = power_meter((display_width*0.05, display_height-100), 10)
# power_meter2 = power_meter((display_width*0.95-50, display_height-100), 10)
# sprites = [pen1, pen2, pointer1, pointer2, power_meter1, power_meter2]


def button(text, x, y, width, height, inactive_color, active_color, action = None):
    cur = pygame.mouse.get_pos()
    #print(cur)
    click = pygame.mouse.get_pressed()

    if x+width > cur[0] > x and y+height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "quit":
                pygame.quit()
                quit()
            if action == "controls":
                game_controls()
            if action == "play":
                gameLoop()
            if action == "main":
                gameIntro()

    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)
  


def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    if size == "small":
        textSurf = smallfont.render(msg, True, color)
    elif size == "medium":
        textSurf = medfont.render(msg, True, color)
    elif size == "large":
        textSurf = largefont.render(msg, True, color)    
    textRect = textSurf.get_rect()
    textRect.center = ((buttonx+(buttonwidth/2)),(buttony+(buttonheight/2)))
    gameDisplay.blit(textSurf, textRect)



def game_controls():
    
    pygame.event.wait()
    while True:
        gameDisplay.fill(black)

        message_to_screen("Controls",
                            green,
                            -150,
                            "large")
        message_to_screen("Hold Spacebar to set power and release to attack",
                            white,
                            -30)
        message_to_screen("Change position of pointer with Up and Down arrows",
                            white,
                            20)
        message_to_screen('Switch Direction with "f"',
                            white,
                            70)
        

        button("Back", 1110,650,100,50,yellow,light_yellow, action="main")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        clock.tick(15)





def gameIntro():
    pygame.mixer.music.load("bg_music.wav")
    pygame.mixer.music.play(-1)
    gameDisplay.fill(black)
    message_to_screen("Dumbbell Fight!!!", 
                                red,
                                -150, 
                                "medium")
    message_to_screen("First one to kick the opponet out 3 times wins!!", 
                        white,
                        10,
                        "small")
    message_to_screen("Press Enter to start", 
                        white,
                        200,
                        "small")

    pygame.event.wait()
    while True:
        button("Controls", 1110, 650, 150, 50, yellow, light_yellow, action = "controls")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        
        
        pygame.display.update()



def gameOver(winner):
    pygame.mixer.music.stop()
    pygame.mixer.music.load("end.wav")
    pygame.mixer.music.play(-1)
    message_to_screen(f"{winner} Wins!!", 
                                red,
                                -20, 
                                "medium")
    message_to_screen("Press C to play again or Q to quit", 
                        black,
                        70,
                        "small")

    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    gameloop()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        
        
        
        pygame.display.update()



def gameloop():
    pygame.mixer.music.load("bg_music.wav")
    pygame.mixer.music.play(-1)

    gameExit = False
    # gameOver = True

    pen1 = pen(display_width*0.3, display_height*0.5, 0, "blue")
    pen2 = pen(display_width*0.7, display_height*0.5, 0, "green")
    pointer1 = pointer((display_width*0.05,display_height*0.5-pen_height),(display_width*0.05,display_height*0.5-pen_height+150))
    pointer2 = pointer((display_width*0.95-50,display_height*0.5-pen_height),(display_width*0.95-50,display_height*0.5-pen_height+150))
    power_meter1 = power_meter((display_width*0.05, display_height-100), 10)
    power_meter2 = power_meter((display_width*0.95-50, display_height-100), 10)
    score = score_board()
    sprites = [pen1, pen2, pointer1, pointer2, power_meter1, power_meter2, score]


    turn = 1
    pointer2.direction = "RIGHT"
    pointer_change = 0
    dist_from_cm = 0
    power1 = 10
    power2 = 10
    power_change = False


    while not gameExit:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    power_change = True
                elif event.key == pygame.K_DOWN:
                        pointer_change = 2
                elif event.key == pygame.K_UP:
                    pointer_change = -2
                elif event.key == pygame.K_f:
                    # print(pointer1.direction)
                    if turn == 1:
                        if pointer1.direction == "LEFT":
                            pointer1.direction = "RIGHT"
                        else:
                            pointer1.direction = "LEFT"
                    elif turn == 2:
                        if pointer2.direction == "LEFT":
                            pointer2.direction = "RIGHT"
                        else:
                            pointer2.direction = "LEFT"


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    power_change = False
                    if turn == 1:
                        velocity, omega = calc_vel_omega(pen1, dist_from_cm, power_meter1.power)
                        move(pen1 , pen2,  velocity, omega,  pointer1.direction, sprites)
                        turn = 2
                        pointer1.dist_from_cm = 0
                        power_meter1.power = 10
                        power1 = 10
                        power_meter2.power = 10
                        power2 = 10
                    elif turn == 2:
                        velocity, omega = calc_vel_omega(pen2, dist_from_cm, power_meter2.power)
                        move(pen2 , pen1,  velocity, omega,  pointer2.direction, sprites)
                        turn = 1
                        pointer2.dist_from_cm = 0
                        power_meter2.power = 10
                        power2 = 10
                        power_meter1.power = 10
                        power1 = 10

                elif event.key == pygame.K_UP:
                        pointer_change = 0
                elif event.key == pygame.K_DOWN:
                        pointer_change = 0
                
        
        # if pen2.angle > 360:
        #     pen2.angle = pen2.angle%360 + omega
        # elif pen2.angle < -360:
        #     pen2.angle = pen2.angle%-360 + omega
        # else:
        #     pen2.angle += omega
        # pen1.x += x_vel
        # pen1.y += y_vel

        if turn == 1:
            if pointer1.pos[1] > pointer1.end[1]-pointer_size:
                pointer1.pos[1] = pointer1.end[1]-pointer_size
            elif pointer1.pos[1] < pointer1.start[1]:
                pointer1.pos[1] = pointer1.start[1]
            else:
                pointer1.pos[1] += pointer_change
            dist_from_cm = pointer1.dist_from_cm
        elif turn == 2:
            if pointer2.pos[1] > pointer2.end[1]-pointer_size:
                pointer2.pos[1] = pointer2.end[1]-pointer_size
            elif pointer2.pos[1] < pointer2.start[1]:
                pointer2.pos[1] = pointer2.start[1]
            else:
                pointer2.pos[1] += pointer_change
            dist_from_cm = pointer2.dist_from_cm

    
        if power_change == True:
            if turn == 1:
                if power1 != 60:
                    power1 += 10
                else:
                    clock.tick(7)
                    power1 = 10
                power_meter1.power = power1
            
            elif turn == 2:
                if power2 != 60:
                    power2 += 10
                else:
                    clock.tick(7)
                    power2 = 10
                power_meter2.power = power2
            clock.tick(7)


        gameDisplay.fill(peach)
        
        if sprites[0].x > display_width*0.78 or sprites[0].x < display_width*0.22 or sprites[0].y > display_height*0.8 or sprites[0].y < display_height*0.2:  #  85 45 JANKY - FIX LATER
            pygame.mixer.Sound.play(ta_da)
            score.score2 += 1
            if score.score2 == 3:
                gameOver("Player 2")
            pen1.x, pen1.y, pen1.angle = display_width*0.3, display_height*0.5, 0
            pen2.x, pen2.y, pen2.angle = display_width*0.7, display_height*0.5, 0
            # gameOver()
        if sprites[1].x > display_width*0.78 or sprites[1].x < display_width*0.22 or sprites[1].y > display_height*0.8 or sprites[1].y < display_height*0.2:  # JANKY - FIX LATER
            pygame.mixer.Sound.play(ta_da)
            score.score1 += 1
            if score.score1 == 3:
                gameOver("Player 1")
            pen1.x, pen1.y, pen1.angle = display_width*0.3, display_height*0.5, 0
            pen2.x, pen2.y, pen2.angle = display_width*0.7, display_height*0.5, 0
            # gameOver()
            
    
        draw_sprites(sprites)


        pygame.display.update()

        #print(clock.get_fps())
        clock.tick(FPS)

    pygame.quit()
    quit()



gameIntro()
