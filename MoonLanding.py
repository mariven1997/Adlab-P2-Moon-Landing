# Importing all the needed packages
import pygame as pg # Pygame is needed to create the game itself, not for any of the math. We could have also done this in a pychart, but we chose the hard way
import numpy as np # Numpy is needed for many of the calculations
import time as t # Time is used very little, but improves the look of some of the animations by making them take longer
import math # Math is used for some of the calculations


Retry = True # Retry is a boolian function that allows the game to repeat when r is pressed, but end when p is pressed
while Retry:
    
    # Assign sprite file names to a list, referenced later to import image files (used to animate the player's moon lander module)
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
    TurnLength = 0.3 # The period of each "turn." Turns constitute the time after a button is pressed (w, a, s, or d). This value can be changed to make the game easier or harder/impossible
    PixelsPerMeter = 8 # The number of pixels in each meter of space
    Xo = SCREEN_WIDTH/2 # The x position of the origin point of the calculations in the coordinate system of the screen in pixels. The screen has an origin point at the top left corner, x increasing to the right, and y down the screen.
    Yo = SCREEN_HEIGHT - 100 # "    " The same as above but with y. We placed it at 100 pixels above the bottom to have enough visible space to be comfortable, but not so much that the initial position was off the screen.
    Mass = DryMass + FMass # Total initial mass, kg
    endpos = np.array([Xo+10*PixelsPerMeter,Yo]) # This is a vector that tells the computer the end position as a function of the Xo and the Yo, as well as the intended landing position (10 meters) multiplied by pixels per meter to scale the displacement to the correct size.
    ShipHeight = 54  # The height of the physical body of the ship, pixels - this is needed in part because the ship sprites include empty texture to incorporate thruster graphics, so the image is significantly larger than the ship itself
    ShipWidth = 34  # The width of the physical body of the ship, pixels
    
    
    # Create space
    backgroundimg = pg.image.load('SpaceBG.png') # Import the background image of space
    background = backgroundimg.get_rect() # Create a rectangle equal to the image size for loading purposes. This is needed in order to place the object
    background.topleft = (0,0) # Create a position for the background (just at the top left corner)
    
    # Create the moon
    moonimg = pg.image.load('Moonscape.png') # Import the image of the moon's surface (thank you Kamryn) You're very welcome Mace
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
        deltaX = PixelsPerMeter*((vX*dT)+(ThrustX*(dT**2))/(2*(Mass+(dM*TimeStep/2)))) # define an equation for a change of position for dT (0.001 seconds). Based on the equation for position in kinematics (x = x0 + v0t + 1/2*at^2). For the Euler approximation, this is changed up to the current equation, where x0 = 0, v0 = the velocity at the start of the 0.001 seconds, and a is determined by thrust (if used)
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
    def update(image, Cycle, ts): # This function updates the screen whenever an animation happens by redrawing all of the objects.
        screen.blit(backgroundimg, (0,0)) # draw the background on the screen
        screen.blit(moonimg, moon) # draw the moon
        pg.draw.rect(screen, (128,0,0), Moonsurface) # draw the line that shows the moon's surface
        pg.draw.rect(screen, (10,128,10), LandingZone) # draw the landing zone
        for i in range(0,iteration): # create a for loop to draw all of the path markers in their respective locations on the screen (iteration is set as a variable later)
            pg.draw.rect(screen, (128,0,0), Path[i])
        if TrajectoryCheck: # if trajectory has been toggled using the t butten, run through a for loop that draws the 90 points of the trajectory line, showing you 30 wait actions into the future.
            for i in range(0,90):
                pg.draw.rect(screen, (0,0,128), Trajectory[i])
        if image != shipimage: # This makes it so that the idle image for the ship can be used in this function along side the animated versions.
            screen.blit(pg.image.load(image[Cycle]), shiprect)
        else: # if I loaded the ship image with a Cycle, it would break the game, since it is a single value, not an array.
            screen.blit(image, shiprect)
        screen.blit(Velocity_Panel.render(f'Current Velocity: Vx = {-Vx:.3f}, Vy = {Vy:.3f}, V = {np.sqrt(Vx**2+Vy**2):.3f} m/s', False, (0, 128, 0)), (0,0)) # Draw the velocity pannel with the current velocity values
        screen.blit(Fuel_Panel.render(f'Fuel Mass: {Mass-DryMass:.2f} kg', False, (0, 128, 0)), (0,30)) # Draw the fuel pannel with the current fuel mass values
        Cycle += 1 # increase the cycle value (cycles whatever animation is being used to the next frame)
        if Cycle >= 5: # reset the cycle if it reaches 5 (which is outside the range for any of our animations)
            Cycle = 0
        pg.display.update() # Update the screen
        t.sleep(ts) # tell the system to wait for a period of time specified in the call of the function (this allows us to make the game run at whatever rate we want with zero being the fastest)
        return Cycle # Return the cycle value
    
        
    # Create an ending Variable, used to determine which ending was achieved
    end = 0
    
    # Create variables for the trajectory tracker
    TrajectoryCheck = False # Create a checker to see if trajectory has been toggled
    Trajectory = [0]*90 # Create a list of 90 values, which will be filled with the 2 by 2 squares that make up the trajectory line. These values also carry the position values for these trajectory markers
    
    
    LoopBuddy = 0 # LoopBuddy tracks the time intervals in the euler approximations
    iteration = 1 # iteration tells you what turn you are on. This is used for placing the path markers
    
    # Create x and y positional change variables
    delX = 0
    delY = 0
    
    Burn = False # Burn is used to get rid of the 1 frame of idle animation between turns if you keep holding a, s, or d
    
    run = True # This is used to tell the game to run (pretty self explanitory by the name). If this is set to false, the while loop that the game runs in will end.
    Playtime = True # This is true as long as you have not won or lost, and allows you to access movement controls.
    while run: # This is the while loop that the game runs in.
        
        
        if end != 2: # 2 is the only of the three endings where the crash animation is active, at which point I do not want to update the screen with the normal ship image
            if Burn: # this gets rid of 1 frame of update (only visual) if you used a thrust command, so that if you are holding a, s, or d, the transition between turns is a seemless animation. (it just looks nicer)
                Burn = False
            else:
                update(shipimage, 4, 0) # Update the ship frame
    
        key = pg.key.get_pressed() # This looks for keypresses
        if key[pg.K_t]: # If t is pressed, the trajectory tracker is activated
            if TrajectoryCheck: # this if/else statment acts as a toggle for the trajectory indicator. Switching TrajectoryCheck to true makes the trajectory line show, whereas switching it to false makes the line not display
                TrajectoryCheck = False
            else:
                TrajectoryCheck = True
            t.sleep(0.15) # This time delay is put in so that if t is pressed, the game does not read the input multiple times. This could have been done better in other ways, but this way works well enough and does not impact the game or calculations, so we chose the easier solution
        
        # The trajectory is calculated every time the game loops through. It is low intensity, so it does not slow down the game (now that we optimised it)
        LoopBuddy = 0 # Loop buddy is set to zero to start the process of the while loop that comes later
        Trajector = np.array([CurrentPos[0],CurrentPos[1]]) # Trajector is an array that is used in calculating the trajectory. It is set to the current value of the CurrentPos vector. We could not have set it equal to the vector itself because when we did, the CurrentPos vector was also adjusted, which was not expected
        delXt = delX # delXt and delYt are values that are used as small displacements for the euler approximation used in the trajectory calculator. They are set to the values of delX and delY because delX and delY are not fully used every time the ship moves. This is because the ship cannot move between pixels, and so we only use the displacement values of delX and delY when they are above 1, after which the displacement is subtracted from the delX or delY. This way, no information is lost because of pixel size being discrete. delX and delY are both measured in pixels.
        delYt = delY
        Vyt = Vy # Vyt and Vxt are set to the current velocities in the x and y directions, so that the actual velocities are not changed during the trajectory calculations
        Vxt = Vx
        Masst = Mass # Masst is set to Mass for the same reason as with Vyt and Vxt
        counter = 0
        while LoopBuddy < 9: # This while loop is used to make the Euler approximation. The trajectory loop iterates 9000 times, effectively giving you a look 30 turns into the future assuming you use no thrust.
            delXt += MotionX(Vxt, 0, TimeStep, Mass, 0) # These statements set delXt and delYt equal to the the sum of themselves and the motion functions given the velocity at that time step, the length of the time step, and the current mass. The 0s are for thrust and burnrate, which are only needed in the function if you are thrusting (which the trajectory does not account for intentionally)
            delYt += MotionY(Vyt, 0, TimeStep, Mass, 0) # as stated before, both delYt and delXt are measured in pixels as float values
            if abs(delXt)>=1: # if either delX or delY are at or above 1 pixel in the size of the displacement, the ship is moved on the screen. This makes the ship's position on the screen an approximation, but because pixels exist, this is necessary. In the trajectory calculations, this same method is used to track the placement of the markers, since they must also be placed at integer locations on the screen (the game would break if you placed them based on a float)
                Trajector += [-math.floor(delXt),0] # every time the if statement is passed, the trajector vector is altered by the floor of the value of delXt (or delYt in the delYt if statement). This makes it so that the trajector vector is always at integer values so that it does not cause errors. Both the delX and delY shif are negative because of the coordinate system we chose. All the math works out.
                delXt = delXt - math.floor(delXt) # to keep consistant, the delXt and delYt variables have whatever value is not large enough to change the position on the screen saved. This makes it so that the information is not lost during the calculations. Even if it is small during each step, with hundreds (or thousands) of steps, the information adds up quite a lot.
            if abs(delYt)>=1: # This statement is the same as the last one but with delYt
                Trajector += [0,-math.floor(delYt)]
                delYt = delYt - math.floor(delYt)
            Vyt = Vyt - g*TimeStep # Vyt is updated based on the acceleration due to gravity by the end of the time step. Vxt is not changed because it is uneffected by any values in the trajectory calculations
            Trajectory[math.floor(LoopBuddy*10)] = pg.Rect((Trajector[0] + 0.5*ShipWidth,Trajector[1] + 0.5*ShipHeight, 2,2)) # The 90 values of the trajectory vector are placed in one at a time.
            LoopBuddy += TimeStep # LoopBuddy is increased by the time step. Once this value reaches 9 on the 9000th iteration, this value ends the while loop
        if Playtime: # When Playtime is false, the controls are locked. This happens when the game ends. Only the r, p, and t buttons are still functional
            
            # The next three large if statements all do the same basic thing. Each one is a statement that thrusts in a direction based on the key pressed.
            # s is for thrust downward
            if key[pg.K_s] == True: # if s is pressed, this statement activates. This constitutes a turn (0.3 seconds).
                Burn = True # Burn is set to true so that the first idle frame is skipped on the next turn (purely visual as explained earlier)
                LoopBuddy = 0 # LoopBuddy is set to zero to start the while loop fresh
                while LoopBuddy < TurnLength:  # This works the same as the trajectory calculation, but here, only 300 calculations are made, coresponding to a turn length of 0.3 seconds.   
                    delX += MotionX(Vx, 0, TimeStep, Mass, -1*BurnRate) # This works just as with the trajectory calculations except thrust is given in the y direction, and the burnrate is applied.
                    delY += MotionY(Vy, Thrust, TimeStep, Mass, -1*BurnRate)
                    if abs(delX)>=1: # As with the trajectory calculations, these two if statements only allow visual position changes in 1 pixel intervals (or more, if you are going fast enough to have the approximation be off by over a pixel, which should never happen in this game)
                        shiprect.move_ip(-math.floor(delX),0) # This function moves the ship according to delX at descrete pixel values
                        CurrentPos += [-math.floor(delX),0] # here, we update the current position vector with the number of pixels that were shifted
                        delX = delX - math.floor(delX) # here, we assign delX to be the difference between the actual value of delX and the number of pixels shifted so that no data is lost
                    if abs(delY)>=1:
                        shiprect.move_ip(0,-math.floor(delY))
                        CurrentPos += [0,-math.floor(delY)]
                        delY = delY - math.floor(delY)
                    if Mass-DryMass>0: # This statement makes it so that you cannot thrust if you don't have any fuel. When this is not true, s, d, and a all act the same way as the wait button, w.
                        Vy = Vy + Thrust*TimeStep/Mass - g*TimeStep # update the y velocity based on gravity and thrust. The x velocity is constant for s.
                        Mass += -1*BurnRate*TimeStep # update the mass based on the burn rate
                        if int(math.floor(LoopBuddy*40)) == round(LoopBuddy*40,3): # This statement reduces the number of full updates made to the screen so that the game runs faster (purely visual and optimization). 40 was chosen arbitrarily to give a good speed and 11 frames of animation in the update function, which is enough to make it seemless to our eyes
                            Cycle = update(BurnUpArt,Cycle,0.025) # We use the update function to update our screen and animate the ship. 0.025 was chosen for the time delay because it is a comfortable animation speed here.
                    else:
                        if int(math.floor(LoopBuddy*40)) == round(LoopBuddy*40,3): # This is the same as the if statement above, but is only activated if the ship is out of fuel, and the update should just be the ship falling with no burn animation
                            update(shipimage, 4, 0.025) # 4 is chosen for the animation arbitrarily (it doesn't matter here)
                        Vy = Vy - g*TimeStep # This is an alternative update to velocity when thrust is no longer available, and gravity is the only thing that effects Vy
                    LoopBuddy += TimeStep   # count up by 1 step
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3))) # This adds a marker to the path indicator at the current position of the ship (specifically at the middle of the image)
                iteration += 1 # Increase the turn counter by 1, indicating you are moving on to the next turn
                
            # a is for thrust left. Almost everything in this is the same as the if statement for s, so we skip over most of the explanation that we went through in the s if statement
            if key[pg.K_a] == True:
                Burn = True
                LoopBuddy = 0
                while LoopBuddy < TurnLength:
                    delX += MotionX(Vx, -1*Thrust, TimeStep, Mass, -1*BurnRate) # Here as well as in the d if statement, thrust is applied horizontally. In this one, thrust is applied as a negative because of how we oriented our coordinates. 
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
                        Vx = Vx - Thrust*TimeStep/Mass # Here and in the d if statement, Vx is effected by thrust, and thus is updated accordingly
                        Mass += -1*BurnRate*TimeStep
                        if int(math.floor(LoopBuddy*40)) == round(LoopBuddy*40,3):
                            Cycle = update(BurnLeftArt,Cycle,0.025)
                    elif int(math.floor(LoopBuddy*40)) == round(LoopBuddy*40,3):
                        update(shipimage, 4, 0.025)
                    Vy = Vy - g*TimeStep # The velocity in the y is always changed by graivty.
                    LoopBuddy += TimeStep   
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
                
            # d is for thrust right. As with the a if statement, we skip most of the explanation that has already been covered, since most things are the same.
            if key[pg.K_d] == True:
                Burn = True
                LoopBuddy = 0
                while LoopBuddy < TurnLength:
                    delX += MotionX(Vx, Thrust, TimeStep, Mass, -1*BurnRate) # Thrust is applied in the positive x direction here (based on the coordinate system that we used for the function)
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
                        if int(math.floor(LoopBuddy*40)) == round(LoopBuddy*40,3):
                            Cycle = update(BurnRightArt,Cycle,0.025)
                    elif int(math.floor(LoopBuddy*40)) == round(LoopBuddy*40,3):
                        update(shipimage, 4, 0.025)
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep   
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
                
            # w is for wait. Most of this is also the same function as the previous three if statements, but it does not have any thrust, so it is more simple. As such, we again skip most of the explanations that have already been covered
            if key[pg.K_w] == True:
                LoopBuddy = 0
                while LoopBuddy < TurnLength:
                    delX += MotionX(Vx, 0, TimeStep, Mass, 0) # as with the trajectory calculator, no thrust is applied
                    delY += MotionY(Vy, 0, TimeStep, Mass, 0)
                    if abs(delX)>=1:
                        shiprect.move_ip(-math.floor(delX),0)
                        CurrentPos += [-math.floor(delX),0]
                        delX = delX - math.floor(delX)
                    if abs(delY)>=1:
                        shiprect.move_ip(0,-math.floor(delY))
                        CurrentPos += [0,-math.floor(delY)]
                        delY = delY - math.floor(delY)
                    if int(math.floor(LoopBuddy*40)) == round(LoopBuddy*40,3):
                        update(shipimage, 4, 0.025)
                    Vy = Vy - g*TimeStep
                    LoopBuddy += TimeStep   
                Path.append(pg.Rect((CurrentPos[0] + 0.5*ShipWidth,CurrentPos[1] + 0.5*ShipHeight, 3,3)))
                iteration += 1
                
            # This if statement checks if you are at the win condition or at the surface of the moon.
            if endpos[0] - PixelsPerMeter<=CurrentPos[0]<=endpos[0] + PixelsPerMeter and endpos[1]+0.5*PixelsPerMeter>=(CurrentPos[1] + 50)>=endpos[1]-0.5*PixelsPerMeter and Playtime: # the parameters here are based on the end position +/- 1 meter in the x and +/-0.5 meters in the y. Since the ship is treated as the upper left corner of it's image, the y condition is moved up by 50 so that it is at the ship's feet
                if np.sqrt(Vy**2+Vx**2) <= 1: # If you are at the win condition (the platform), this if statement checks if your velocity (found as the root of the sum of the squares of both x and y velocities) is low enough to land safely. Otherwise, you crash.
                    print("yay!! :)")
                    end = 1 # ending 1 does nothing as of now, but was going to show an animation of a guy walking out of the space ship after landing. That would have been a far more complex and time consuming animation than the others, and was therefore not ready
                    Playtime = False # When any ending is achived, playtime is set to false so that the motion controls can no longer be accessed.
                else:
                    print("You died :(")
                    end = 2 # ending 2 is a crash, and starts the crash animation. This happens whenever you are going too fast, not just when you are on the landing platform
                    Playtime = False
            elif CurrentPos[1]>=endpos[1]-50 and not endpos[0] - PixelsPerMeter<=CurrentPos[0]<=endpos[0] + PixelsPerMeter: # This elif statment checks if you are at the surface of the moon. If you are, you lose whether you are landing at a safe speed or not. The exception here is if you are within the area of the platform, at which point, you may be lower than the surface (by 0.5 meter at most)
                if np.sqrt(Vy**2+Vx**2) <= 1: # If you are outside the landing zone, you can land safely (Ignoring the craters in the art), but you still lose as you did not land in the right location
                    print("You lose >:(")
                    end = 3
                    Playtime = False
                else:
                    print("You died :(")
                    end = 2
                    Playtime = False
      
        # This if statment runs through the death animation. Another if statement for end 1 and end 3 would have been created if we had animated them           
        if end == 2: 
            Cycle = update(WreckArt,Cycle, 0.1)
        # This for loop looks for the p and r keys being pressed. Once either is pressed, the run loop ends.
        for event in pg.event.get():
            if key[pg.K_p]:
                run = False 
                Retry = False # if p is pressed, both while loops that contain the game will end.
            if key[pg.K_r]:
                run = False # This statment just ends the while loop that the game runs in, which means the restart loop is still going and the game starts over again.
    
pg.quit() # if the restart loop ends, this closes the game window.
