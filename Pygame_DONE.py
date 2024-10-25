from asyncio import Semaphore
import math
import time
import threading
from datetime import datetime
import random
import pygame
from utils import scale_image, blit_rotate_center

# Import pngs
# track and track border must be scaled the same (9 is placeholder)
start_time = time.time()
runMultiplayer = False
runSimulation = False
inp = input("type  M for Multiplayer, S for Simulation")
try:
    if inp == "m":
        runMultiplayer=True
    if inp == "s":
        runSimulation=True
    print("You entered:", inp)
except KeyboardInterrupt:
    print("\nProgram interrupted. Exiting gracefully.")

GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)

POWERUP = scale_image(pygame.image.load("imgs/powerup.png"), 0.25)
ROADBLOCK = scale_image(pygame.image.load("imgs/cone.png"), 1.5)

TRACK = scale_image(pygame.image.load("imgs/pixilart-track.png"), 9)

TRACK_BORDER = scale_image(pygame.image.load("imgs/pixilart-emptyTrack.png"), 9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = scale_image(pygame.image.load("imgs/finish.png"), 5.8)
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (35,5)

Car1 = pygame.image.load("imgs/red-car.png")
Car2 = pygame.image.load("imgs/purple-car.png")


WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height() # set width, height of track image
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))  # window = width, height
pygame.display.set_caption("Multithreading Car Race")

FPS = 60

class AbstractCars: 
    #from project code
    mutex_lock = False
    race_Over = False
    #end from project code
    def __init__(self, max_vel, rotation_vel, row, symbol):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 1
        #from project code
        self.pos = 0
        self.row = row
        self.symbol = symbol
        #end from project code

    #from project code
    def start(self):
        while self.pos < 7:

            # sleep timer is used to detemine speed
            time.sleep(random.randint(1, 6))

            if AbstractCars.race_Over:
                print(f"Car {self.symbol} realizes the race is over")
                break

            if AbstractCars.mutex_lock == False:
                AbstractCars.mutex_lock = True
                # critical section
                self.increase_pos()
                AbstractCars.mutex_lock = False
            else:
                print(f"\ncar {self.symbol}'s movement was momentarily blocked: busy waiting")
                # busy waiting checking every 0.1 seconds
                while (AbstractCars.mutex_lock == True):
                    time.sleep(0.1)

                AbstractCars.mutex_lock = True
                # critical seciton
                self.increase_pos()
                AbstractCars.mutex_lock = False

        if AbstractCars.race_Over == False:
            AbstractCars.race_Over = True
            print(f"game finished car {self.symbol} won the race!")

    def increase_pos(self):
        # test for mutex lock: slows down process so it has the opportunity to block
        time.sleep(1)

        # blank line
        print()

        if random.randint(1, 10) < 5:
            # change lanes
            print(f"Car {self.symbol} changes lanes")

            if self.row == 0:  # checks if in lane 0
                if arr[1][self.pos] == 0: #checks if space in lane 1 is  empty
                    arr[self.row][self.pos] = 0 #leaves current space in array empty
                    self.row = 1  #changes to lane 1
                    arr[self.row][self.pos] = self.symbol  #updating new position in array
                    for i in range(0,23):
                        self.rotate(left=True)
                        time.sleep(.01)
                    for i in range(0,76):
                        self.move_forward()
                        time.sleep(.01)
                    for i in range(0,23):
                        self.rotate(right=True)
                        time.sleep(.01)
                elif arr[1][self.pos] == 4:  # checks if spot is a powerup
                    arr[self.row][self.pos] = 0 #leaves current spot as empty in the array
                    self.row = 1 #changes row
                    #we keep the array as the powerup
                    print(f"Car {self.symbol} picks up a powerup")
                    #animation
                    for i in range(0, 23):
                        self.rotate(left=True)
                        time.sleep(.01)
                    for i in range(0, 76):
                        self.move_forward()
                        time.sleep(.01)
                    for i in range(0, 23):
                        self.rotate(right=True)
                        time.sleep(0.01)
                    # will try to move forward again
                    if arr[self.row][self.pos + 1] == 0:  # checks if spot ahead is empty
                        self.pos = self.pos + 1 #changes self position 1 forward
                        arr[self.row][self.pos] = self.symbol #saves it's new location in the array
                        print(f"Car {self.symbol} boosts forward using the powerup")
                        for i in range(0, 25):
                            #
                            self.move_forward()
                            #
                            time.sleep(.01)
                        else:
                            print(f"Car {self.symbol} tried to boost forward with the powerup but was blocked, boosts around")
                            self.row = 0 #goes back to original lane
                            arr[self.row][self.pos] = self.symbol #saves new location in array
                            for i in range(0, 23):
                                self.rotate(right=True)
                                time.sleep(.01)
                            for i in range(0, 76):
                                self.move_forward()
                                time.sleep(.01)
                            for i in range(0, 23):
                                self.rotate(left=True)
                                time.sleep(.01)
                else: #adjacent lane is blocked
                    for i in range(0,10):
                        self.rotate(left=True)
                        time.sleep(.01)
                    for i in range(0, 10):
                        self.rotate(right=True)
                        time.sleep(.01)
                    print("Car", self.symbol, "tried to switch lanes but was blocked")
            else:
                if arr[0][self.pos] == 0: #if lane 0 is empty
                    arr[self.row][self.pos] = 0 #leave old position empty in the array
                    self.row = 0 #move to lane 0
                    arr[self.row][self.pos] = self.symbol #save new position in the array
                    #animation
                    for i in range(0,23):
                        self.rotate(right=True)
                        time.sleep(.01)
                    for i in range(0,76):
                        self.move_forward()
                        time.sleep(.01)
                    for i in range(0,23):
                        self.rotate(left=True)
                        time.sleep(.01)
                elif arr[0][self.pos] == 4:  # checks if spot is a powerup
                    arr[self.row][self.pos] = 0 # leaves current spot as empty in the array
                    self.row = 0  # changes row to row 0
                    # we keep the array as the powerup
                    #animation
                    for i in range(0, 23):
                        self.rotate(right=True)
                        time.sleep(.01)
                    for i in range(0, 76):
                        self.move_forward()
                        time.sleep(.01)
                    for i in range(0, 23):
                        self.rotate(left=True)
                        time.sleep(.01)
                    # will try to move forward again
                    if arr[self.row][self.pos + 1] == 0:  # checks if spot ahead is empty
                        self.pos = self.pos + 1 #increase position by 1
                        arr[self.row][self.pos] = self.symbol #save new position to the array
                        print(f"Car {self.symbol} boosts forward using the powerup")
                        for i in range(0, 25):
                            #
                            self.move_forward()
                            #
                            time.sleep(.01)
                    else:
                        print(f"Car {self.symbol} tried to boost forward with the powerup but was blocked, boosts around")
                        self.row = 1  # goes back to original lane
                        arr[self.row][self.pos] = self.symbol  # saves new location in array
                        for i in range(0, 23):
                            self.rotate(left=True)
                            time.sleep(.01)
                        for i in range(0, 76):
                            self.move_forward()
                            time.sleep(.01)
                        for i in range(0, 23):
                            self.rotate(right=True)
                            time.sleep(.01)
                else:
                    for i in range(0,10):
                        self.rotate(right=True)
                        time.sleep(.01)
                    for i in range(0, 10):
                        self.rotate(left=True)
                        time.sleep(.01)
                    print("Car", self.symbol, "tried to switch lanes but was blocked")
        #Moving Forward
        if arr[self.row][self.pos + 1] == 0:  # checks if spot ahead is empty
            arr[self.row][self.pos] = 0
            self.pos = self.pos + 1
            arr[self.row][self.pos] = self.symbol
            print(f"Car {self.symbol} moves")
            for i in range(0,25):
                #
                self.move_forward()
                #
                time.sleep(.01)
        elif arr[self.row][self.pos + 1] == 4: #checks if spot is a powerup
            #same as move forward
            arr[self.row][self.pos] = 0
            self.pos = self.pos + 1
            arr[self.row][self.pos] = self.symbol
            print(f"Car {self.symbol} moved and picked up a powerup")
            for i in range(0, 25):
                #
                self.move_forward()
                #
                time.sleep(.01)
            #will try to move forward again
            if arr[self.row][self.pos + 1] == 0:  # checks if spot ahead is empty
                arr[self.row][self.pos] = 4
                self.pos = self.pos + 1
                arr[self.row][self.pos] = self.symbol
                print(f"Car {self.symbol} boosts forward using the powerup")
                for i in range(0, 25):
                    #
                    self.move_forward()
                    #
                    time.sleep(.01)
            else:
                print(f"Car {self.symbol} tried to boost with the powerup but was blocked")
        else:
            print(f"Car {self.symbol} tried to move but was blocked")

        print(time.time() - start_time)
        print_arr()

    #end from project code
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

class CreateCar(AbstractCars):  #PlayerCar
    IMG = Car1
    START_POS = (450, 730)

# bounce car if collision occurs (needs decceleration in order to work)
#       def bounce(self): 
#           self.vel = -self.vel
#           self.move()

class CreateCar2(AbstractCars):
    IMG = Car2
    START_POS = (150, 730)

    def draw(self, win):
        super().draw(win)


def draw(win, images, created_car, created_car2):
    for img, pos in images:
        win.blit(img, pos)

    created_car.draw(win)
    created_car2.draw(win)
    pygame.display.update() # display images

def move_player1(player_car):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_j] & runMultiplayer:
        player_car.rotate(left=True)   # turn left
    if keys[pygame.K_l] & runMultiplayer:
        player_car.rotate(right=True)  #turn right
    if keys[pygame.K_i] & runMultiplayer:
        player_car.move_forward()

def move_player2(player_car):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] & runMultiplayer:
        player_car.rotate(left=True)  
    if keys[pygame.K_d] & runMultiplayer:
        player_car.rotate(right=True)  
    if keys[pygame.K_w] & runMultiplayer:
        player_car.move_forward()

#from  project code
def print_arr():
    for row in arr:
        print(row)

global rows, cols
rows, cols = (2, 8)
arr = [[0 for i in range(cols)] for j in range(rows)]

arr[0][0] = 1
arr[1][0] = 2
obsticle_X = random.randint(0,1)
obsticle_Y = random.randint(1,6)
powerup_X = random.randint(0,1)
powerup_Y = random.randint(1,6)
if (powerup_X == obsticle_X) & (powerup_Y == obsticle_Y):
    if powerup_X == 1:
        powerup_X = 0
    else:
        powerup_X = 1
arr[obsticle_X][obsticle_Y]=3 #obsticle
arr[powerup_X][powerup_Y]=4
#end from project code
won = False

clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION),(POWERUP,(450-int(300*powerup_X),750-int(100*powerup_Y))),(ROADBLOCK,(450-int(300*obsticle_X),750-int(100*obsticle_Y)))]
created_car = CreateCar(4, 4,0,1) # (4, 4) placeholder velocity   # player_car
created_car2 = CreateCar2(4, 4,1,2)


while runMultiplayer:
    clock.tick(FPS)

    draw(WINDOW, images, created_car, created_car2)


    WINDOW.blit(GRASS, (0,0)) # display grass in window
    WINDOW.blit(TRACK,(0,0)) # display track
    WINDOW.blit(Car1,(0,0)) # display car 1
    WINDOW.blit(Car2,(0,0)) # display car 2
    #WINDOW.blit(ROADBLOCK, (0, 0))  # display roadblock in window
    #WINDOW.blit(POWERUP, (0, 0))  # display roadblock in window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break


    move_player1(created_car)
    move_player2(created_car2)

    if created_car.collide(TRACK_BORDER_MASK) != None or created_car2.collide(TRACK_BORDER_MASK) != None:
        if won == True:
            break
        else: 
            print("collide")

    if created_car.collide(FINISH_MASK, *FINISH_POSITION) != None:
        print("Player 1 Wins!")
        won = True

    if created_car2.collide(FINISH_MASK, *FINISH_POSITION) != None:
        print("Player 2 Wins!")
        won = True

if runSimulation:
    # from project code
    t1 = threading.Thread(target=created_car.start)
    t2 = threading.Thread(target=created_car2.start)
    t1.start()
    t2.start()
    # end from project code
    while runSimulation:
        clock.tick(FPS)

        draw(WINDOW, images, created_car, created_car2)


        WINDOW.blit(GRASS, (0, 0))  # display grass in window
        WINDOW.blit(TRACK, (0, 0))  # display track
        WINDOW.blit(Car1, (0, 0))  # display car 1
        WINDOW.blit(Car2, (0, 0))  # display car 2
        WINDOW.blit(ROADBLOCK, (0, 0))  # display roadblock in window
        WINDOW.blit(POWERUP, (0, 0))  # display roadblock in window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

pygame.quit