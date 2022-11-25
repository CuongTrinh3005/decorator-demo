from app.main.util.decorators import cache_it
from app.main.util.decorators import time_it


@time_it
@cache_it
def factorial(num):
    fact = 1
    while num > 0:
        fact = fact * num
        num = num - 1
    return fact


@time_it
def factorial_no_cache(num):
    fact = 1
    while num > 0:
        fact = fact * num
        num = num - 1
    return fact


if __name__ == "__main__":
    print("Running these in the first time:")
    factorial(10000)
    factorial_no_cache(10000)

    print("\nRunning these in the second time:")
    factorial(10000)
    factorial_no_cache(10000)
