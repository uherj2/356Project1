import time
from datetime import datetime
import random
import threading
start_time = time.time()


class Car:

    def __init__(self):
        self.pos = 0

    def start(self, symbol, row):
        while self.pos < 4:
            time.sleep(random.randint(1, 10))
            self.increase_pos(symbol, int(row))

    def increase_pos(self, symbol, row):
        arr[row][self.pos] = 0
        arr[row][self.pos + 1] = symbol
        print(f"\nCar {symbol} moves")
        print(time.time() - start_time)
        print_arr()

        self.pos = self.pos + 1


def print_arr():
    for row in arr:
        print(row)


# initialize 2d array

global rows, cols
rows, cols = (2, 5)
arr = [[0 for i in range(cols)] for j in range(rows)]

arr[0][0] = 1

car_1 = Car()
car_2 = Car()
t1 = threading.Thread(target=car_1.start, args=(1, 0))
t2 = threading.Thread(target=car_2.start, args=(2, 1))

t1.start()
t2.start()





