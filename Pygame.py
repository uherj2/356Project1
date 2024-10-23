import pygame
import time
import math
from utils import scale_image, blit_rotate_center

# Import pngs
# track and track border must be scaled the same (9 is placeholder)
GRASS = scale_image(pygame.image.load("imgs/grass.jpg"), 2.5)

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

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = .1

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
    
    if keys[pygame.K_j]:    
        player_car.rotate(left=True)   # turn left
    if keys[pygame.K_l]:
        player_car.rotate(right=True)  #turn right
    if keys[pygame.K_i]:
        player_car.move_forward()

def move_player2(player_car):
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a]:    
        player_car.rotate(left=True)  
    if keys[pygame.K_d]:
        player_car.rotate(right=True)  
    if keys[pygame.K_w]:
        player_car.move_forward()


won = False
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION)]
created_car = CreateCar(4, 4) # (4, 4) placeholder velocity   # player_car
created_car2 = CreateCar2(4, 4)

while run:
    clock.tick(FPS)

    draw(WINDOW, images, created_car, created_car2)

    WINDOW.blit(GRASS, (0,0)) # display grass in window
    WINDOW.blit(TRACK,(0,0)) # display track 
    WINDOW.blit(Car1,(0,0)) # display car 1
    WINDOW.blit(Car2,(0,0)) # display car 2


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

pygame.quit