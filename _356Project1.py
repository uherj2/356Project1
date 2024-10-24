from asyncio import Semaphore
import time
from datetime import datetime
import random
import threading

start_time = time.time()

class Car:

    #initialize mutex_lock as a static variable and as false
    mutex_lock = False
    race_Over = False

    def __init__(self, row, symbol):
        self.pos = 0
        self.row = row
        self.symbol = symbol

    def start(self):
            while self.pos < 4:

                #sleep timer is used to detemine speed
                #sleep timer is alo reused to simulate busy waiting
                time.sleep(random.randint(1, 6))

                if Car.race_Over:
                    print(f"Car {self.symbol} realizes the race is over")
                    break

                if Car.mutex_lock == False:
                    Car.mutex_lock = True
                    #critical section
                    self.increase_pos()
                    Car.mutex_lock = False
                else:
                    print(f"car {self.symbol}'s movement was momentarily blocked")

            if Car.race_Over == False: 
                Car.race_Over = True
                print(f"game finished car {self.symbol} won the race!")

    def increase_pos(self):
        #test for mutex lock: slows down process so it has the opportunity to block
        time.sleep(1)

        #blank line
        print()

        if random.randint(1, 10) < 5:
            # change lanes
            print(f"Car {self.symbol} changes lanes")
        
            
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
        
        if arr[self.row][self.pos + 1] == 0: #checks if spot ahead is empty
            arr[self.row][self.pos] = 0
            self.pos = self.pos + 1
            arr[self.row][self.pos] = self.symbol
            print(f"Car {self.symbol} moves")
        else: 
            print(f"Car {self.symbol} tried to move but was blocked")

        print(time.time() - start_time)
        print_arr()

def print_arr():
    for row in arr:
        print(row)


# initialize 2d arrayj
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