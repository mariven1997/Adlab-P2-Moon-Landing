# Importing all the needed packages
import pygame as pg # Pygame is needed to create the game itself, not for any of the math. We could have also done this in a pychart, but we chose the hard way
import numpy as np # Numpy is needed for many of the calculations
import time as t # Time is used very little, but improves the look of some of the animations by making them take longer
import math # Math is used for some of the calculations
#TODO
# Stop thrust when fuel is empty
# Detect Hitting the Ground
# Aesthetics
# The line plotty thing
# Fuel Monitor
# Desired Landing Site
#


Retry = True # Retry is a boolian function that allows the game to repeat when r is pressed, but end when p is pressed
while Retry:
    
    # Import all of the various moon lander images (used to animate the player's moon lander module)
    BurnRightArt = ["R1.png", "R2.png", "R3.png", "R4.png", "R5.png"]
    BurnLeftArt = ["L1.png", "L2.png", "L3.png", "L4.png", "L5.png"]
    BurnUpArt = ["V1.png", "V2.png", "V3.png", "V4.png", "V5.png"]
    WreckArt = ["Wreck1.png", "Wreck2.png", "Wreck3.png", "Wreck4.png", "Wreck5.png"]
    IdleArt = "Lander.png"
    
    # Initialize pygame
    pg.init()
    
    # Create the height and width of the window that the game runs in
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 850
    
    # Establishing Variables
    n = 13 #Letter value of last name (13 for m and 15 for o)
    X = -10 #Initial Position, m
    Y = 30*(1. + 4.*n%5) #Inital Altitude, m
    Vx = 0 #Initial velocity in x, m/s
    Vy = 0 #Initial velocity in y, m/s
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
    
    
    # Create space
    backgroundimg = pg.image.load('SpaceBG.png')
    background = backgroundimg.get_rect()
    background.topleft = (0,0)
    
    # Create the moon
    # moon = pg.Rect((pos[0],pos[1] + 0.5*PixelsPerMeter,1000,100))
    moonimg = pg.image.load('Moonscape.png')
    moon = moonimg.get_rect()
    moon.topleft = (0,600)
    
    # Create the win condition
    LandingZone = pg.Rect((endpos[0] - PixelsPerMeter,endpos[1],2*PixelsPerMeter + ShipWidth,PixelsPerMeter))
    
    # Create moon surface indicator line
    Moonsurface = pg.Rect((0,endpos[1] + 0.5*PixelsPerMeter,600,1))
    
    
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
    background = pg.image.load('SpaceBG.png').convert_alpha    # This will be where we load whatever background image of the moon we get
    #backrect = background.get_rect()
    
    # Create a current position array for the lander
    CurrentPos = np.array([Xo + X*PixelsPerMeter, Yo - Y*PixelsPerMeter])
    
    # Create Path Markers
    Path = [0]
    Path[0] = pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3))
    
    
    # Create an update system for images
    Cycle = 0
    def update(image, Cycle, ts):
        # screen.fill((0,0,0))
    #    pg.draw.rect(screen, (0, 0, 0), backrect)
        screen.blit(backgroundimg, (0,0))
        # pg.draw.rect(screen, (120,120,120), moon)
        screen.blit(moonimg, moon)
        pg.draw.rect(screen, (128,0,0), Moonsurface)
        pg.draw.rect(screen, (10,128,10), LandingZone)
        for i in range(0,iteration):
            pg.draw.rect(screen, (128,0,0), Path[i])
        screen.blit(pg.image.load(image[Cycle]), shiprect)
        screen.blit(Velocity_Panel.render(f'Current Velocity: Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s', False, (0, 128, 0)), (0,0))
        screen.blit(Fuel_Panel.render(f'Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0)), (0,30))
        Cycle += 1
        if Cycle >= 5:
            Cycle = 0
        
        pg.display.update()
        t.sleep(ts)
        return Cycle
    
        
    # Create an ending Variable
    end = 0
    
    TrajectoryCheck = False
    Trajectory = np.zeros(90)
    Trajectory = Trajectory.tolist()
    
    LoopBuddy = 0
    iteration = 1
    
    # Create x and y positional change variables
    delX = 0
    delY = 0
    
    run = True
    Playtime = True
    while run:
        
        
        if end != 2:
            # screen.fill((0,0,0))
            # Place the cold dark vacume of outer space
            screen.blit(backgroundimg, (0,0))
            # Place the moon
            screen.blit(moonimg, moon)
            #pg.draw.rect(screen, (120,120,120), moon)
            # Place moon surface indicator
            pg.draw.rect(screen, (128,0,0), Moonsurface)
            # Place the win condition
            pg.draw.rect(screen, (10,128,10), LandingZone)
            # Place path markers
            for i in range(0,iteration):
                pg.draw.rect(screen, (128,0,0), Path[i])
            if TrajectoryCheck:
                for i in range(0,90):
                    pg.draw.rect(screen, (0,0,128), Trajectory[i])
            # Place ship
            screen.blit(shipimage, shiprect)
            # Place info dump
            screen.blit(Velocity_Panel.render(f'Current Velocity: Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s', False, (0, 128, 0)), (0,0))
            screen.blit(Fuel_Panel.render(f'Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0)), (0,30))
        
        #Tring to make it plot a parabola (calculated elsewhere) that shows projected trajectory
        #pg.draw.lines(screen, (50,50,50), False, PathTrack, width=5)
        
        
        
        
        key = pg.key.get_pressed()
        if Playtime:
            if key[pg.K_t]:
                LoopBuddy = 0
                Trajector = np.array([CurrentPos[0],CurrentPos[1]])
                delXt = delX
                delYt = delY
                Vyt = Vy
                Vxt = Vx
                Masst = Mass
                while LoopBuddy <= 9:
                    delXt += MotionX(Vxt, 0, TimeStep*10, Mass, 0)
                    delYt += MotionY(Vyt, 0, TimeStep*10, Mass, 0)
                    if abs(delXt)>=1:
                        Trajector += [-math.floor(delXt),0]
                        delXt = delXt - math.floor(delXt)
                    if abs(delYt)>=1:
                        Trajector += [0,-math.floor(delYt)]
                        delYt = delYt - math.floor(delYt)
                    Vyt = Vyt - g*TimeStep*10
                    LoopBuddy += TimeStep*10
                    if math.floor((LoopBuddy*100))%10 != 90:
                        Trajectory[math.floor(LoopBuddy*100/10)-1] = pg.Rect((Trajector[0] + 0.5*ShipWidth,Trajector[1] + 0.5*ShipHeight, 2,2))
                TrajectoryCheck = True
            
            # Place the ship
            if key[pg.K_s] == True:
                TrajectoryCheck = False
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
                        if int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                            update(BurnUpArt,math.floor(LoopBuddy*120/3)%5,0)
                    elif int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                        screen.fill((0,0,0))
                        screen.blit(backgroundimg, (0,0))
                        # pg.draw.rect(screen, (120,120,120), moon)
                        screen.blit(moonimg, moon)
                        pg.draw.rect(screen, (128,0,0), Moonsurface)
                        pg.draw.rect(screen, (10,128,10), LandingZone)
                        for i in range(0,iteration):
                            pg.draw.rect(screen, (128,0,0), Path[i])
                        screen.blit(shipimage, shiprect)
                        screen.blit(Velocity_Panel.render(f'Current Velocity: Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s', False, (0, 128, 0)), (0,0))
                        screen.blit(Fuel_Panel.render(f'Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0)), (0,30))
                        pg.display.update() 
                    else:
                        Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep    
                    PathTrack.append([X, Y])
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
            if key[pg.K_a] == True:
                TrajectoryCheck = False
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
                        #update(BurnLeftArt,math.floor(LoopBuddy*50)%5,0)
                        if int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                            update(BurnLeftArt,math.floor(LoopBuddy*120/3)%5,0)
                    elif int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                        # screen.fill((0,0,0))
                        screen.blit(backgroundimg, (0,0))
                        # pg.draw.rect(screen, (120,120,120), moon)
                        screen.blit(moonimg, moon)
                        pg.draw.rect(screen, (128,0,0), Moonsurface)
                        pg.draw.rect(screen, (10,128,10), LandingZone)
                        for i in range(0,iteration):
                            pg.draw.rect(screen, (128,0,0), Path[i])
                        screen.blit(shipimage, shiprect)
                        screen.blit(Velocity_Panel.render(f'Current Velocity: Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s', False, (0, 128, 0)), (0,0))
                        screen.blit(Fuel_Panel.render(f'Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0)), (0,30))
                        pg.display.update()
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep   
                    PathTrack.append([X, Y])
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
            if key[pg.K_d] == True:
                TrajectoryCheck = False
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
                        #update(BurnRightArt,math.floor(LoopBuddy*50)%5,0)
                        if int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                            update(BurnRightArt,math.floor(LoopBuddy*120/3)%5,0)
                    elif int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                        screen.fill((0,0,0))
                        screen.blit(backgroundimg, (0,0))
                        # pg.draw.rect(screen, (120,120,120), moon)
                        screen.blit(moonimg, moon)
                        pg.draw.rect(screen, (128,0,0), Moonsurface)
                        pg.draw.rect(screen, (10,128,10), LandingZone)
                        for i in range(0,iteration):
                            pg.draw.rect(screen, (128,0,0), Path[i])
                        screen.blit(shipimage, shiprect)
                        screen.blit(Velocity_Panel.render(f'Current Velocity: Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s', False, (0, 128, 0)), (0,0))
                        screen.blit(Fuel_Panel.render(f'Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0)), (0,30))
                        pg.display.update()
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep      
                    PathTrack.append([X, Y])
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
            if key[pg.K_w] == True:
                #TrajectoryCheck = False
                LoopBuddy = 0
                while LoopBuddy <= TurnLength:
                    # W key should wait
                    delX += MotionX(Vx, 0, TimeStep, Mass, 0) #-1*BurnRate)
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
                    if int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                        screen.fill((0,0,0))
                        screen.blit(backgroundimg, (0,0))
                        # pg.draw.rect(screen, (120,120,120), moon)
                        screen.blit(moonimg, moon)
                        pg.draw.rect(screen, (128,0,0), Moonsurface)
                        pg.draw.rect(screen, (10,128,10), LandingZone)
                        for i in range(0,iteration):
                            pg.draw.rect(screen, (128,0,0), Path[i])
                        if TrajectoryCheck:
                            for i in range(0,90):
                                pg.draw.rect(screen, (0,0,128), Trajectory[i])
                        screen.blit(shipimage, shiprect)
                        screen.blit(Velocity_Panel.render(f'Current Velocity: Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s', False, (0, 128, 0)), (0,0))
                        screen.blit(Fuel_Panel.render(f'Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0)), (0,30))
                        pg.display.update()
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep      
                    PathTrack.append([X, Y])
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
            if endpos[0] - PixelsPerMeter<=CurrentPos[0]<=endpos[0] + PixelsPerMeter and endpos[1]+0.5*PixelsPerMeter>=(CurrentPos[1] + 50)>=endpos[1]-0.5*PixelsPerMeter and Playtime:
                if np.sqrt(Vy**2+Vx**2) <= 1:
                    print("yay!! :)")
                    end = 1
                    Playtime = False
                else:
                    print("You died :(")
                    end = 2
                    Playtime = False
            elif CurrentPos[1]>=endpos[1]-50 and not endpos[0] - PixelsPerMeter<=CurrentPos[0]<=endpos[0] + PixelsPerMeter:
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
            if key[pg.K_p]:
                run = False 
                Retry = False
            if key[pg.K_r]:
                run = False
        pg.display.update()
    
pg.quit()
