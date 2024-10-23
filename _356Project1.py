from asyncio import Semaphore
from imp import acquire_lock, release_lock
import time
from datetime import datetime
import random
import threading

start_time = time.time()

class Car:

    def __init__(self, row, symbol):
        self.pos = 0
        self.row = row
        self.symbol = symbol

    def start(self):
        while self.pos < 4:
            time.sleep(random.randint(1, 10))
            self.increase_pos()

    def increase_pos(self):

        if random.randint(1, 10) < 5:
            # change lanes
            print(f"\nCar {self.symbol} change lanes")
           
            acquire_lock #mutex for accessing the grid
            if self.row == 0: #checks if space is empty
                if arr[1][self.pos] == 0: 
                    arr[self.row][self.pos] = 0
                    self.row = 1 #sets row to the row we just checked
                    arr[self.row][self.pos] = self.symbol #changing the array
                else:
                    print("Car",self.symbol,"tried to switch lanes but was blocked")
            else:
                if arr[0][self.pos] == 0: 
                    arr[self.row][self.pos] = 0
                    self.row = 0 
                    arr[self.row][self.pos] = self.symbol
                else:
                    print("Car",self.symbol,"tried to switch lanes but was blocked")
            release_lock
            

        acquire_lock
        if arr[self.row][self.pos + 1] == 0: #checks if spot ahead is empty
            arr[self.row][self.pos] = 0
            self.pos = self.pos + 1
            arr[self.row][self.pos] = self.symbol
            print(f"\nCar {self.symbol} moves")
        else: 
            print(f"\nCar {self.symbol} tried to move but was blocked")

        print(time.time() - start_time)
        print_arr()

        release_lock

def print_arr():
    for row in arr:
        print(row)


# initialize 2d array

global rows, cols
rows, cols = (2, 5)
arr = [[0 for i in range(cols)] for j in range(rows)]

arr[0][0] = 1
arr[1][0] = 2


car_1 = Car(0, 1)
car_2 = Car(1, 2)
t1 = threading.Thread(target=car_1.start)
t2 = threading.Thread(target=car_2.start)

t1.start()
t2.start()

