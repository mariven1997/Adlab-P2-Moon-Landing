import pygame as pg
import numpy as np
import time as t


# Initialize pygame
pg.init()

# Create the height and width of the window that the game runs in
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800


# Establishing Variables
n = 13 #Letter value of last name (13 for m and 15 for o)
X = -10 #Initial Position, m
Y = 30*(1. + 4.*n%5) #Inital Altitude, m
Vx = 0 #Initial velocity, m/s
Vy = 0 #Initial velocity, m/s
Mass = (1 + 0.1*n%5)*10**4 #Initial mass, kg
FMass = 4*(1 + 0.1*n%6)*10**3 #Initial mass of the fuel
Thrust = 4.8*(1 + 0.05*n%4)*10**4 #Thrust supplied by the engine
BurnRate = 5 #Fuel burn rate, kg/s
pos = np.array([0,700])
g = 1.62 # m/s^2
EngineIsFiring = False
EngineOrientation = "D"
TimeStep = 0.001
TurnLength = 0.25


# Create the moon
moon = pg.Rect((pos[0],pos[1],1000,100))


# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Moon Lander')

# Establishes ship as a rectangle and also gives it a graphics
shipimage = pg.image.load("TempImage.png").convert_alpha()
shiprect = shipimage.get_rect()
shiprect.topleft = (50, 50)

# Defining Position Functions, dM should be negative
def MotionX(vX, ThrustX, dT, Mass, dM):
    deltaX = (vX*dT)+(ThrustX*(dT**2))/(2*(Mass+(dM/2)))
    return deltaX
def MotionY(vY, ThrustY, dT, Mass, dM):
    deltaY = (vY*dT)+(ThrustY*(dT**2))/(2*(Mass+(dM/2)))-(g*(dT**2)/2)
    return deltaY

# load images
# Background
# background_img = pg.image.load('').convert_alpha    # This will be where we load whatever background image of the moon we get




run = True
while run:
    
    screen.fill((0,0,0))
    
    # Place the moon
    pg.draw.rect(screen, (120,120,120), moon)
    # Place the ship
    pg.draw.rect(screen, (50,50,50), shiprect)
    screen.blit(shipimage, shiprect)
    
    #Tring to make it plot a parabola (calculated elsewhere) that shows projected trajectory
    pg.draw.lines(screen, (50,50,50), False, ((1,1), (10, 20), (75,300)), width=5)
    
    key = pg.key.get_pressed()
    if key[pg.K_s] == True:
        LoopBuddy = 0
        while LoopBuddy <= TurnLength:        
            #S key should rotate the engine to face DOWN
            shiprect.move_ip(MotionX(Vx, 0, TimeStep, Mass, -1*BurnRate), MotionY(Vy, Thrust, TimeStep, Mass, -1*BurnRate))
            Mass += -1*BurnRate
            Vy = Vy + Thrust*TimeStep - g*TimeStep
            LoopBuddy += TimeStep
    if key[pg.K_a] == True:
        LoopBuddy = 0
        while LoopBuddy <= TurnLength:
#A key should rotate the engine to face RIGHT
            shiprect.move_ip((MotionX(Vx, -1*Thrust, TimeStep, Mass, -1*BurnRate), MotionY(Vy, 0, TimeStep, Mass, -1*BurnRate)))
            Mass += -1*BurnRate
            Vx = Vx - Thrust*TimeStep
            Vy = Vy - g*TimeStep
            LoopBuddy += TimeStep
    if key[pg.K_d] == True:
        LoopBuddy = 0
        while LoopBuddy <= TurnLength:
            #D key should rotate the engine to face LEFT
            shiprect.move_ip((MotionX(Vx, Thrust, TimeStep, Mass, -1*BurnRate), MotionY(Vy, 0, TimeStep, Mass, -1*BurnRate)))
            Mass += -1*BurnRate
            Vx = Vx + Thrust*TimeStep
            Vy = Vy - g*TimeStep
            LoopBuddy += TimeStep
    if key[pg.K_w] == True:
        LoopBuddy = 0
        while LoopBuddy <= TurnLength:
            # W key should wait
            shiprect.move_ip(MotionX(Vx, 0, TimeStep, Mass, -1*BurnRate), MotionY(Vy, 0, TimeStep, Mass, 0))
            Vy = Vy - g*TimeStep
            LoopBuddy += TimeStep
    
    
    for event in pg.event.get():
        if key[pg.K_p] == True:
            run = False
            
    t.sleep(0.003)     
    pg.display.update()
pg.quit()
