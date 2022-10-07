import random
import math

def exponential_random(rate):
    """Generates an exponential random variable at the given rate"""
    return -(1 / rate) * math.log(1.0 - random.random())
