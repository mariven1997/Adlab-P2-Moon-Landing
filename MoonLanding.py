
import pygame as pg
import numpy as np
import time as t
import math
#TODO
# Stop thrust when fuel is empty
# Detect Hitting the Ground
# Aesthetics
# The line plotty thing
# Fuel Monitor
# Desired Landing Site
#



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
DryMass = (1 + 0.1*n%5)*10**4 #Initial mass, kg
FMass = 4*(1 + 0.1*n%6)*10**3 #Initial mass of the fuel
Thrust = 4.8*(1 + 0.05*n%4)*10**4 #Thrust supplied by the engine
BurnRate = 5 #Fuel burn rate, kg/s
pos = np.array([0,700])
g = 1.62 # m/s^2
EngineIsFiring = False
EngineOrientation = "D"
TimeStep = 0.001
TurnLength = 0.25
PixelsPerMeter = 30
Xo = SCREEN_WIDTH/2 # in pixels
Yo = 700 # "   "
Mass = DryMass + FMass
endpos = np.array([Xo+10*PixelsPerMeter,Yo-1.5*PixelsPerMeter])

# A list that keeps track of positional data for the line plot
PathTrack = [[X, Y]]

# Create the moon
moon = pg.Rect((pos[0],pos[1],1000,100))

# Create the win condition
Landing = pg.Rect((endpos[0],endpos[1],2*PixelsPerMeter,PixelsPerMeter))


# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Moon Lander')

# Establishes ship as a rectangle and also gives it a graphics
shipimage = pg.image.load("Lander.png").convert_alpha()
shiprect = shipimage.get_rect()
shiprect.topleft = (0, 50)

# Defining Position Functions, dM should be negative
def MotionX(vX, ThrustX, dT, Mass, dM):
    deltaX = PixelsPerMeter*((vX*dT)+(ThrustX*(dT**2))/(2*(Mass+(dM*TimeStep/2))))
    pg.display.update()
    t.sleep(0.0001)
    return deltaX
def MotionY(vY, ThrustY, dT, Mass, dM):
    deltaY = PixelsPerMeter*((vY*dT)+((ThrustY*(dT**2))/(2*(Mass+(dM*TimeStep/2))))-(g*(dT**2)/2))
    pg.display.update()
    t.sleep(0.0001)
    return deltaY

# load images
# Background
# background_img = pg.image.load('').convert_alpha    # This will be where we load whatever background image of the moon we get

# Create a current position array for the lander
CurrentPos = np.array([0.,50.])

run = True
while run:
    
    screen.fill((0,0,0))
    
    # Place the moon
    pg.draw.rect(screen, (120,120,120), moon)
    # Place the ship
    pg.draw.rect(screen, (50,50,50), shiprect)
    screen.blit(shipimage, shiprect)
    # Place the win condition
    pg.draw.rect(screen, (10,128,10), Landing)
    
    #Tring to make it plot a parabola (calculated elsewhere) that shows projected trajectory
    #pg.draw.lines(screen, (50,50,50), False, PathTrack, width=5)
    
    key = pg.key.get_pressed()
    if key[pg.K_s] == True:
        LoopBuddy = 0
        delX = 0
        delY = 0
        while LoopBuddy <= TurnLength:        
            #S key should rotate the engine to face DOWN
            delX += MotionX(Vx, 0, TimeStep, Mass, -1*BurnRate)
            delY += MotionY(Vy, Thrust, TimeStep, Mass, -1*BurnRate)
            if abs(delX)>=1:
                shiprect.move_ip(-math.floor(delX),0)
                CurrentPos += [-math.floor(delX),0]
                delX = delX - math.floor(delX)
            if abs(delY)>=1:
                shiprect.move_ip(0,-math.floor(delY))
                CurrentPos += [0,-math.floor(delY)]
                delY = delY - math.floor(delY)
            Mass += -1*BurnRate*TimeStep
            Vy = Vy + Thrust*TimeStep/Mass - g*TimeStep
            LoopBuddy += TimeStep    
            PathTrack.append([X, Y])
        t.sleep(0.05)
    if key[pg.K_a] == True:
        LoopBuddy = 0
        delX = 0
        delY = 0
        while LoopBuddy <= TurnLength:
            #A key should rotate the engine to face RIGHT
            delX += MotionX(Vx, -1*Thrust, TimeStep, Mass, -1*BurnRate)
            delY += MotionY(Vy, 0, TimeStep, Mass, -1*BurnRate)
            if abs(delX)>=1:
                shiprect.move_ip(-math.floor(delX),0)
                CurrentPos += [-math.floor(delX),0]
                delX = delX - math.floor(delX)
            if abs(delY)>=1:
                shiprect.move_ip(0,-math.floor(delY))
                CurrentPos += [0,-math.floor(delY)]
                delY = delY - math.floor(delY)
            Mass += -1*BurnRate*TimeStep
            Vx = Vx - Thrust*TimeStep/Mass
            Vy = Vy - g*TimeStep
            LoopBuddy += TimeStep   
            PathTrack.append([X, Y])
        t.sleep(0.05)
    if key[pg.K_d] == True:
        LoopBuddy = 0
        delX = 0
        delY = 0
        while LoopBuddy <= TurnLength:
            #D key should rotate the engine to face LEFT
            delX += MotionX(Vx, Thrust, TimeStep, Mass, -1*BurnRate)
            delY += MotionY(Vy, 0, TimeStep, Mass, -1*BurnRate)
            if abs(delX)>=1:
                shiprect.move_ip(-math.floor(delX),0)
                CurrentPos += [-math.floor(delX),0]
                delX = delX - math.floor(delX)
            if abs(delY)>=1:
                shiprect.move_ip(0,-math.floor(delY))
                CurrentPos += [0,-math.floor(delY)]
                delY = delY - math.floor(delY)
            Mass += -1*BurnRate*TimeStep
            Vx = Vx + Thrust*TimeStep/Mass
            Vy = Vy - g*TimeStep
            LoopBuddy += TimeStep      
            PathTrack.append([X, Y])
        t.sleep(0.05)
    if key[pg.K_w] == True:
        LoopBuddy = 0
        delX = 0
        delY = 0
        while LoopBuddy <= TurnLength:
            # W key should wait
            delX += MotionX(Vx, 0, TimeStep, Mass, -1*BurnRate)
            delY += MotionY(Vy, 0, TimeStep, Mass, 0)
            if abs(delX)>=1:
                shiprect.move_ip(-math.floor(delX),0)
                CurrentPos += [-math.floor(delX),0]
                delX = delX - math.floor(delX)
            if abs(delY)>=1:
                shiprect.move_ip(0,-math.floor(delY))
                CurrentPos += [0,-math.floor(delY)]
                delY = delY - math.floor(delY)
            Vy = Vy - g*TimeStep
            LoopBuddy += TimeStep      
            PathTrack.append([X, Y])
        t.sleep(0.05)
    print(CurrentPos)
    print(endpos)
    if endpos[0]<=CurrentPos[0]<=endpos[0]+2*PixelsPerMeter and endpos[1]>=CurrentPos[1]>=endpos[1]-1*PixelsPerMeter:
        print("yay")
        break
    for event in pg.event.get():
        if key[pg.K_p] == True:
            run = False
            
    t.sleep(0.05)     
    #pg.display.update()
pg.quit()
