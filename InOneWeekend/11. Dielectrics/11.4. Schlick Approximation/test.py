import math
import random
from timeit import timeit

x = random.random()


def f():
    x**5


def g():
    math.pow(x, 5)


print(timeit(f))
print(timeit(g))
