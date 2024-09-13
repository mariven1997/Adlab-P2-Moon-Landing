import pygame as pg
import numpy as np
import time as t


# Initialize pygame
pg.init()

# Create the height and width of the window that the game runs in
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000



pos = np.array([475,475])
g = 1.62 # m/s^2


# Create the ship
ship = pg.Rect((pos[0],pos[1],50,50))


# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Moon Lander')

# Establishes ship as a rectangle and also gives it a graphics
shipimage = pg.image.load("TempImage.png").convert_alpha()
shiprect = shipimage.get_rect()
shiprect.topleft = (50, 50)


# load images
# Background
# background_img = pg.image.load('').convert_alpha    # This will be where we load whatever background image of the moon we get

# Establishing Variables
X = -10 #Initial Position, m
Y = 30 #Inital Altitude, m
Vx = 0 #Initial velocity, m/s
Vy = 0 #Initial velocity, m/s
Mass = 5 #Initial mass, kg
BurnRate = 5 #Fuel burn rate, kg/s


run = True
while run:
    
    screen.fill((0,0,0))
    
    # Place the ship
    pg.draw.rect(screen, (50,50,50), ship)
    pg.draw.rect(screen, (50,50,50), shiprect)
    screen.blit(shipimage, shiprect)
    
    key = pg.key.get_pressed()
    if key[pg.K_s] == True:
        shiprect.move_ip(0,-1)
    if key[pg.K_w] == True:
        shiprect.move_ip(0,1)
    if key[pg.K_a] == True:
        shiprect.move_ip(1,0)
    if key[pg.K_d] == True:
        shiprect.move_ip(-1,0)
    
    for event in pg.event.get():
        if key[pg.K_p] == True:
            run = False
            
    t.sleep(0.003)     
    pg.display.update()
pg.quit()
