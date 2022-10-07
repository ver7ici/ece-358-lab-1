import random
import math

def exponential_random(rate):
    return -(1 / rate) * math.log(1.0 - random.random())
