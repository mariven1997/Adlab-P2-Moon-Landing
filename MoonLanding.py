
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

BurnRightArt = ["R1.png", "R2.png", "R3.png", "R4.png", "R5.png"]
BurnLeftArt = ["L1.png", "L2.png", "L3.png", "L4.png", "L5.png"]
BurnUpArt = ["V1.png", "V2.png", "V3.png", "V4.png", "V5.png"]
WreckArt = ["Wreck1.png", "Wreck2.png", "Wreck3.png", "Wreck4.png", "Wreck5.png"]
IdleArt = "Lander.png"
Cycle = 0

# Initialize pygame
pg.init()

# Create the height and width of the window that the game runs in
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 850

# Establishing Variables
n = 13 #Letter value of last name (13 for m and 15 for o)
X = -10 #Initial Position, m
Y = 30*(1. + 4.*n%5) #Inital Altitude, m
Vx = 0 #Initial velocity, m/s
Vy = 0 #Initial velocity, m/s
DryMass = (1 + 0.1*n%5)*10**4 #Initial mass, kg
FMass = 4*(1 + 0.1*n%6)*10**3 #Initial mass of the fuel
Thrust = 4.8*(1 + 0.05*n%4)*10**4 #Thrust supplied by the engine
BurnRate = 500 #Fuel burn rate, kg/s
pos = np.array([0,SCREEN_HEIGHT - 100])
g = 1.62 # m/s^2
EngineIsFiring = False
EngineOrientation = "D"
TimeStep = 0.001
TurnLength = 0.3
PixelsPerMeter = 8
Xo = SCREEN_WIDTH/2 # in pixels
Yo = SCREEN_HEIGHT - 100 # "   "
Mass = DryMass + FMass
endpos = np.array([Xo+10*PixelsPerMeter,Yo])
ShipHeight = 54  #In pixels
ShipWidth = 34  #In pixels

# A list that keeps track of positional data for the line plot
PathTrack = [[X, Y]]

# Create the moon
moon = pg.Rect((pos[0],pos[1] + 0.5*PixelsPerMeter,1000,100))

# Create the win condition
LandingZone = pg.Rect((endpos[0] - 0.5*ShipWidth,endpos[1],2*PixelsPerMeter + ShipWidth,PixelsPerMeter))


# Create the screen
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Moon Lander')

# Establishes ship as a rectangle and also gives it a graphics
shipimage = pg.image.load(IdleArt).convert_alpha()
shiprect = shipimage.get_rect()
shiprect.topleft = (Xo + X*PixelsPerMeter - 50, Yo - Y*PixelsPerMeter)

# Create the info dump
pg.font.init()
Velocity_Panel = pg.font.SysFont('Roboto', 30)
Fuel_Panel = pg.font.SysFont('Roboto', 30)

# Defining Position Functions, dM should be negative
def MotionX(vX, ThrustX, dT, Mass, dM):
    deltaX = PixelsPerMeter*((vX*dT)+(ThrustX*(dT**2))/(2*(Mass+(dM*TimeStep/2))))
    pg.display.update()
    return deltaX
def MotionY(vY, ThrustY, dT, Mass, dM):
    deltaY = PixelsPerMeter*((vY*dT)+((ThrustY*(dT**2))/(2*(Mass+(dM*TimeStep/2))))-(g*(dT**2)/2))
    pg.display.update()
    return deltaY

# load images
# Background
# background_img = pg.image.load('').convert_alpha    # This will be where we load whatever background image of the moon we get

# Create a current position array for the lander
CurrentPos = np.array([Xo + X*PixelsPerMeter, Yo - Y*PixelsPerMeter])


# Create an update system for images
Cycle = 0
def update(image, Cycle, ts):
    screen.fill((0,0,0))
    pg.draw.rect(screen, (120,120,120), moon)
    pg.draw.rect(screen, (10,128,10), LandingZone)
    screen.blit(pg.image.load(image[Cycle]), shiprect)
    Cycle += 1
    if Cycle >= 5:
        Cycle = 0
    
    pg.display.update()
    t.sleep(ts)
    return Cycle

    
# Create an ending Variable
end = 0

# Create x and y positional change variables
delX = 0
delY = 0

run = True
Playtime = True
while run:
    
    screen.fill((0,0,0))
    
    # Place the moon
    pg.draw.rect(screen, (120,120,120), moon)
    # Place the win condition
    pg.draw.rect(screen, (10,128,10), LandingZone)
    if end == 0:
        screen.blit(shipimage, shiprect)
    
    
    #Tring to make it plot a parabola (calculated elsewhere) that shows projected trajectory
    #pg.draw.lines(screen, (50,50,50), False, PathTrack, width=5)
    
    
    
    
    key = pg.key.get_pressed()
    if Playtime:
        # Place the ship
        if key[pg.K_s] == True:
            LoopBuddy = 0
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
                if Mass-DryMass>0:
                    Vy = Vy + Thrust*TimeStep/Mass - g*TimeStep
                    Mass += -1*BurnRate*TimeStep
                    update(BurnUpArt,math.floor(LoopBuddy*100)%5,0)
                else:
                    Vy = Vy - g*TimeStep
                LoopBuddy += TimeStep    
                PathTrack.append([X, Y])
        if key[pg.K_a] == True:
            LoopBuddy = 0
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
                if Mass-DryMass>0:
                    Vx = Vx - Thrust*TimeStep/Mass
                    Mass += -1*BurnRate*TimeStep
                    update(BurnLeftArt,math.floor(LoopBuddy*100)%5,0)
                Vy = Vy - g*TimeStep
                LoopBuddy += TimeStep   
                PathTrack.append([X, Y])
        if key[pg.K_d] == True:
            LoopBuddy = 0
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
                if Mass-DryMass>0:
                    Vx = Vx + Thrust*TimeStep/Mass
                    Mass += -1*BurnRate*TimeStep
                    update(BurnRightArt,math.floor(LoopBuddy*100)%5,0)
                Vy = Vy - g*TimeStep
                LoopBuddy += TimeStep      
                PathTrack.append([X, Y])
        if key[pg.K_w] == True:
            LoopBuddy = 0
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
                    shipimage = pg.image.load(IdleArt).convert_alpha()
                screen.fill((0,0,0))
                pg.draw.rect(screen, (120,120,120), moon)
                pg.draw.rect(screen, (10,128,10), LandingZone)
                screen.blit(shipimage, shiprect)
                pg.display.update()
                Vy = Vy - g*TimeStep
                LoopBuddy += TimeStep      
                PathTrack.append([X, Y])
        if endpos[0] - PixelsPerMeter - 0.5*ShipWidth<=CurrentPos[0]<=endpos[0] + PixelsPerMeter - 0.5*ShipWidth and endpos[1]+0.5*PixelsPerMeter>=(CurrentPos[1] + 50)>=endpos[1]-0.5*PixelsPerMeter and Playtime:
            if np.sqrt(Vy**2+Vx**2) <= 1:
                print("yay!! :)")
                end = 1
                Playtime = False
            else:
                print("You died :(")
                end = 2
                Playtime = False
        elif CurrentPos[1]>=endpos[1]-50 and not endpos[0]<=CurrentPos[0]<=endpos[0]+2*PixelsPerMeter-ShipWidth:
            if np.sqrt(Vy**2+Vx**2) <= 1:
                print("You lose >:(")
                end = 3
                Playtime = False
            else:
                print("You died :(")
                end = 2
                Playtime = False
    if end == 2:
        Cycle = update(WreckArt,Cycle, 0.15)
    for event in pg.event.get():
        if key[pg.K_p] == True:
            run = False
    text_surface = Velocity_Panel.render(f'Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s, Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0))
    screen.blit(text_surface, (0,0))    
    pg.display.update()
pg.quit()
