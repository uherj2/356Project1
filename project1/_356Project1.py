from asyncio import Semaphore
import time
from datetime import datetime
import random
import threading

start_time = time.time()

class Car:

    # initialize mutex_lock as a static variable and as false
    # True and False is used instead of 0 and 1 in examples
    mutex_lock = False
    race_Over = False

    def __init__(self, row, symbol, arr):
        self.pos = 0
        self.row = row
        self.symbol = symbol
    
        self.arr = arr

    def start(self):
            while self.pos < 9: # Array Column count - 1

                #sleep timer is used to detemine speed
                time.sleep(random.randint(1, 6))

                #checks to see if race is over
                if Car.race_Over:
                    break

                # Mutex lock protects the shared array by limiting access to one car a time
                # If a car is blocked from accessing the array, it does busy waiting
                # The car gets to move immedietly afterward for sake of fairness

                if Car.mutex_lock == False:
                    Car.mutex_lock = True
                    #critical section
                    self.increase_pos()
                    Car.mutex_lock = False
                else:
                    print(f"\ncar {self.symbol}'s movement was momentarily blocked: busy waiting")
                    #busy waiting checking every 0.1 seconds
                    while(Car.mutex_lock == True):
                        time.sleep(0.1)

                    Car.mutex_lock = True
                    #critical seciton
                    self.increase_pos()
                    Car.mutex_lock = False

            # This is acting as another more simplified mutex lock
            # Since only one car needs to access the critical section (finishing the race),
            # Once race_over is declared True, the other car cannot access critical section and the game ends
            if Car.race_Over == False: 
                Car.race_Over = True
                print(f"game finished car {self.symbol} won the race!")
            else:
                print(f"Car {self.symbol} realizes the race is over")

    def increase_pos(self):
        #test for mutex lock: slows down process so it has the opportunity to block
        time.sleep(1)

        #blank line
        print()

        if random.randint(1, 10) < 5:
            # change lanes
            print(f"Car {self.symbol} changes lanes")
        
            
            if self.row == 0: #checks if space is empty
                if self.arr[1][self.pos] == 0: 
                    self.arr[self.row][self.pos] = 0
                    self.row = 1 #sets row to the row we just checked
                    self.arr[self.row][self.pos] = self.symbol #changing the self.array
                else:
                    print("Car",self.symbol,"tried to switch lanes but was blocked")
            else:
                if self.arr[0][self.pos] == 0: 
                    self.arr[self.row][self.pos] = 0
                    self.row = 0 
                    self.arr[self.row][self.pos] = self.symbol
                else:
                    print("Car",self.symbol,"tried to switch lanes but was blocked")
        
        if self.arr[self.row][self.pos + 1] == 0: #checks if spot ahead is empty
            self.arr[self.row][self.pos] = 0
            self.pos = self.pos + 1
            self.arr[self.row][self.pos] = self.symbol
            print(f"Car {self.symbol} moves")
        else: 
            print(f"Car {self.symbol} tried to move but was blocked")

        print(f"Time: {int(time.time() - start_time)} seconds")
        self.print_arr()

    def print_arr(self):
        for row in self.arr:
            print(row)


# initialize 2d array
# game currently works with two Cars: change lane function will have to be updated to work with more

global rows, cols
rows, cols = (2, 10)
arr = [[0 for i in range(cols)] for j in range(rows)]

arr[0][0] = 1
arr[1][0] = 2

car_1 = Car(0, 1, arr)
car_2 = Car(1, 2, arr)

t1 = threading.Thread(target=car_1.start)
t2 = threading.Thread(target=car_2.start)

t1.start()
t2.start()
