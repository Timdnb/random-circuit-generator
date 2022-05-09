from re import L
import numpy as np
import pygame as pg
import math

def pol2cart(rho, phi):
    if phi > math.pi:
        phi = phi-2*math.pi
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    if phi < 0:
        phi = phi+2*math.pi
    return(rho, phi)

# Pygame
pg.init()

# Screen
w_scr = 1100
h_scr = 500
res = (w_scr, h_scr)
screen = pg.display.set_mode(res)
screen_rect = screen.get_rect()
pg.display.set_caption("XY to RTHETA")

white = (255,255,255)
green = '#8FCF4C'

# Draw axes
pg.draw.rect(screen, green, (0,0,500,500))
pg.draw.line(screen, white, (250,0), (250,500), 4)
pg.draw.line(screen, white, (0,250), (500,250), 4)

pg.draw.rect(screen, green, (600,0,500,500))
pg.draw.line(screen, white, (600,0), (600,500), 4)
pg.draw.line(screen, white, (600,500), (1100,500), 4)

last_pos = None
last_phi = 0

while True:
    # Press escape to exit simulation
    pg.event.pump()

    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
        exit()

    if keys[pg.K_SPACE]:
        pg.time.wait(3000)

    # Click with the mouse to add density
    mouse = pg.mouse.get_pressed()
    mouse_pos = pg.mouse.get_pos()

    # Draw
    if (mouse==(1,0,0) or mouse==(1,1,0)):
        # Draw in xy plane
        if (mouse_pos[0] < 500):
            if last_pos != None:
                x1,y1 = (mouse_pos[0]/500)*20-10, (mouse_pos[1]/500)*-20+10
                rho1,phi1 = cart2pol(x1,y1)
                x1s = 600+(phi1/math.pi)*250
                y1s = -25*math.sqrt(2)*rho1+500

                if abs(last_phi - phi1) > math.pi:
                    last_phi = phi1
                    last_pos = None
                    continue
                else:
                    x2,y2 = (last_pos[0]/500)*20-10, (last_pos[1]/500)*-20+10
                    rho2,phi2 = cart2pol(x2,y2)
                    x2s = 600+(phi2/math.pi)*250
                    y2s = -25*math.sqrt(2)*rho2+500
                    pg.draw.line(screen, white, (x2s,y2s), (x1s,y1s), 4)
                last_phi = phi1
                pg.draw.line(screen, white, last_pos, mouse_pos, 4)
            last_pos = mouse_pos
        # # Draw in rtheta plane
        # elif (mouse_pos[0] > 600):
        #     if last_pos != None:
        #         phi1,rho1 = ((mouse_pos[0]-600)/500)*math.pi*2, (mouse_pos[1]/500)*-5*math.sqrt(8)+5*math.sqrt(8)
        #         x1,y1 = pol2cart(rho1,phi1)
        #         # print(phi1, rho1, x1, y1)
        #         x1s = (x1/10)*250+250
        #         y1s = (y1/10)*-250+250

        #         phi2,rho2 = ((last_pos[0]-600)/500)*math.pi*2, (last_pos[1]/500)*-25*math.sqrt(2)+25*math.sqrt(2)
        #         x2,y2 = pol2cart(rho2,phi2)
        #         x2s = (x2/10)*250+250
        #         y2s = (y2/10)*-250+250
        #         # print(x1s, y1s, x2s, y2s)
        #         pg.draw.line(screen, white, (x2s,y2s), (x1s,y1s), 4)
        #         last_phi = phi1
        #         pg.draw.line(screen, white, last_pos, mouse_pos, 4)
        #     last_pos = mouse_pos
        else:
            last_pos = None
    else:
        last_pos = None
    pg.display.flip()