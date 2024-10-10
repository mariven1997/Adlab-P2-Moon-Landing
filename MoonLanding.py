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
    
    # Establishing Variables: ", " means "measured in" (ie: "mass measured in kg" would be "mass, kg")
    n = 13 #Letter value of last name (13 for m and 15 for o)
    X = -10 #Initial Horizantal  Position, m
    Y = 30*(1. + 4.*n%5) #Inital Altitude, m
    Vx = 0 #Initial velocity in x, m/s
    Vy = 0 #Initial velocity in y, m/s
    DryMass = (1 + 0.1*n%5)*10**4 #Dry mass, kg
    FMass = 4*(1 + 0.1*n%6)*10**3 #Initial mass of the fuel, kg
    Thrust = 4.8*(1 + 0.05*n%4)*10**4 #Thrust supplied by the engine, N
    BurnRate = 500 #Fuel burn rate, kg/s
    g = 1.62 # Gravitational acceleration near the moon's surface, m/s^2
    TimeStep = 0.001 # The period of time used as the steps in the Euler Approximations for the motion calculations. 0.001 was used as a very small time step to create low error in the approximation within every calculation.
    TurnLength = 0.3 # The period of each "turn." Turns constitute the time after a button is pressed (w, a, s, or d)
    PixelsPerMeter = 8 # The number of pixels in each meter of space
    Xo = SCREEN_WIDTH/2 # The x position of the origin point of the calculations in the coordinate system of the screen in pixels. The screen has an origin point at the top left corner, x increasing to the right, and y down the screen.
    Yo = SCREEN_HEIGHT - 100 # "    " The same as above but with y. We placed it at 100 pixels above the bottom to have enough visible space to be comfortable, but not so much that the initial position was off the screen.
    Mass = DryMass + FMass # Total initial mass, kg
    endpos = np.array([Xo+10*PixelsPerMeter,Yo]) # This is a vector that tells the computer the end position as a function of the Xo and the Yo, as well as the intended landing position (10 meters) multiplied by pixels per meter to scale the displacement to the correct size.
    ShipHeight = 54  # The height of the physical body of the ship, pixels
    ShipWidth = 34  # The width of the physical body of the ship, pixels
    
    
    # Create space
    backgroundimg = pg.image.load('SpaceBG.png') # Import the background image of space
    background = backgroundimg.get_rect() # Create a rectangle equal to the image size for loading purposes. This is needed in order to place the object
    background.topleft = (0,0) # Create a position for the background (just at the top left corner)
    
    # Create the moon
    moonimg = pg.image.load('Moonscape.png') # Import the image of the moon's surface (thank you Kamryn)
    moon = moonimg.get_rect() # Create a rectangle equal to the image size
    moon.topleft = (0,600) # Create a position for the moon image. This is 250 pixels above the bottom of the screen, since the image is 250 pixels tall.
    
    # Create the win condition
    LandingZone = pg.Rect((endpos[0] - PixelsPerMeter,endpos[1],2*PixelsPerMeter + ShipWidth,PixelsPerMeter)) # This is the landing site, which we chose to be 1 by 6.25 meters. This is based on the +/- 0.5 meters in the y direction and +/- 1 meter in the x direction plus the width of the ship (which allows the ship to effectively be treated as a point per the prompt)
    
    # Create moon surface indicator line
    Moonsurface = pg.Rect((0,endpos[1] + 0.5*PixelsPerMeter,600,1)) # This was created once the image of the moon's surface was created, since it does not allow you to see where you will crash (because of perspective). It is only 1 pixel tall because it only needs to indicate where you will start crashing
    
    # Create the screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Generate the display screen
    pg.display.set_caption('Moon Lander') # Name the window
    
    # Establishes ship as a rectangle and also gives it a graphics
    shipimage = pg.image.load(IdleArt).convert_alpha() # Load the ship image and make it a controlable entity
    shiprect = shipimage.get_rect() # Create a rectangle of size equal to the ship image
    shiprect.topleft = (Xo + X*PixelsPerMeter - 50, Yo - Y*PixelsPerMeter) # create a position for the ship to start in (this is based on the intended starting positions statements (X and Y))
    
    # Create the info dump
    pg.font.init() # Initialize font
    Velocity_Panel = pg.font.SysFont('Roboto', 30) # set the font for the velocity panel
    Fuel_Panel = pg.font.SysFont('Roboto', 30) # set the font for the fuel panel
    
    # Defining Position Functions, dM should be negative
    def MotionX(vX, ThrustX, dT, Mass, dM):
        deltaX = PixelsPerMeter*((vX*dT)+(ThrustX*(dT**2))/(2*(Mass+(dM*TimeStep/2)))) # define an equation for a change of position for dT (0.001 seconds). Based on the equation for position in kinimatics (x = x0 + v0t + 1/2*at^2). For the Euler approximation, this is changed up to the current equation, where x0 = 0, v0 = the velocity at the start of the 0.001 seconds, and a is determined by thrust (if used)
        return deltaX # return the value of the change
    def MotionY(vY, ThrustY, dT, Mass, dM):
        deltaY = PixelsPerMeter*((vY*dT)+((ThrustY*(dT**2))/(2*(Mass+(dM*TimeStep/2))))-(g*(dT**2)/2)) # This is the same as the x motion equation except with an additional subtraction based on gravity (which will always effect the change in y)
        return deltaY
    
    # Create a current position array for the lander
    CurrentPos = np.array([Xo + X*PixelsPerMeter, Yo - Y*PixelsPerMeter])
    
    # Create Path Markers
    Path = [pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3))] # create a list with one value. The value is a square that is 3 by 3 pixels and set at the initial position of the lander. This list is appended every turn with a new square at whatever is the current position of the lander, and each square is shown on the screen to show the path of the lander.
    
    
    # Create an update system for images
    Cycle = 0 # create a variable for tracking which image is being used in an animation
    def update(image, Cycle, ts): # This function updates the screen whenever an animation happens. It fills 
        screen.blit(backgroundimg, (0,0))
        screen.blit(moonimg, moon)
        pg.draw.rect(screen, (128,0,0), Moonsurface)
        pg.draw.rect(screen, (10,128,10), LandingZone)
        for i in range(0,iteration):
            pg.draw.rect(screen, (128,0,0), Path[i])
        if TrajectoryCheck:
            for i in range(0,90):
                pg.draw.rect(screen, (0,0,128), Trajectory[i])
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
            # Place the cold dark vacume of outer space
            screen.blit(backgroundimg, (0,0))
            # Place the moon
            screen.blit(moonimg, moon)
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
        
        
        
        
        
        
        key = pg.key.get_pressed()
        if key[pg.K_t]:
            if TrajectoryCheck:
                TrajectoryCheck = False
            else:
                TrajectoryCheck = True
            t.sleep(0.1)
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
                        if int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                            update(BurnUpArt,math.floor(LoopBuddy*120/3)%5,0.025)
                    elif int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                        screen.blit(backgroundimg, (0,0))
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
                        t.sleep(0.015)
                    else:
                        Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep   
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
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
                        if int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                            update(BurnLeftArt,math.floor(LoopBuddy*120/3)%5,0.025)
                    elif int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                        screen.blit(backgroundimg, (0,0))
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
                        t.sleep(0.015)
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep   
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
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
                        if int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                            update(BurnRightArt,math.floor(LoopBuddy*120/3)%5,0.025)
                    elif int(math.floor(LoopBuddy*120/3)) == round(LoopBuddy*120/3,3):
                        screen.blit(backgroundimg, (0,0))
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
                        t.sleep(0.015)
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep   
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
            if key[pg.K_w] == True:
                LoopBuddy = 0
                while LoopBuddy <= TurnLength:
                    # W key should wait
                    delX += MotionX(Vx, 0, TimeStep, Mass, 0)
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
                        screen.blit(backgroundimg, (0,0))
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
                        t.sleep(0.025)
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep   
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
            Cycle = update(WreckArt,Cycle, 0.1)
        for event in pg.event.get():
            if key[pg.K_p]:
                run = False 
                Retry = False
            if key[pg.K_r]:
                run = False
        pg.display.update()
    
pg.quit()
