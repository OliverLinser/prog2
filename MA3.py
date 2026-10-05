#!/usr/bin/env python3
""" MA3.py

Student: Oliver Linsér
Mail: oliver.linser@hotmail.se
Reviewed by: 
Date reviewed:

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
import numpy as np
from statistics import mean 
from time import perf_counter as pc
from functools import reduce
from numba import njit
import multiprocessing as mp
import concurrent.futures as future

""" Instructions Linux server/git
To enter Linux server: ssh olli9516@gullviva.it.uu.se
Enter Studium A, password
Enter correct map: cd prog2
If no updates simply run ./MA3.py

If changes have been made: in the powershell in visual studio enter:
git add .
git commit -m "Uppdaterat koden"
git push

In the powershell with Linux server type:
git checkout -- MA3.py
git pull
chmod 755 MA3.py
./MA3.py

If sometthing does not work enter:
sed -i -e 's/\r$//' MA3.py in the SSH window
"""

# Exc1
def approximate_pi(n):
    # n is the number of points

    # Write your code here
    x_coordinates_in = []
    y_coordinates_in = []

    x_coordinates_out = []
    y_coordinates_out = []

    x = 0
    y = 0

    n_c = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            n_c += 1
            x_coordinates_in.append(x)
            y_coordinates_in.append(y)
        else:
            x_coordinates_out.append(x)
            y_coordinates_out.append(y)
    plt.scatter(x_coordinates_in, y_coordinates_in, color="red", s = 10)
    plt.scatter(x_coordinates_out, y_coordinates_out, color="blue", s = 10)
    plt.axis("equal")
    plt.savefig(f"pi_approximation_{n}.png")
    plt.show()
    print(n_c)
    return 4*n_c/n
    

# Exc2, approximation

def sphere_volume(n, d): 
    # n is the number of points

    # d is the number of dimensions of the sphere 
    f = lambda x: x**2
    x_coordinates = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    inside_points = lambda p: 1 if reduce(lambda a, b: a + b, map(f, p)) <= 1 else 0
    num_of_inside_points = map(inside_points, x_coordinates)
    n_c = reduce(lambda a, b: a+b, num_of_inside_points)

    return (2**d)*n_c/n
#Exc2, real value
def hypersphere_exact(n, d):
    # n is the number of points
    numerator = np.pi**(d/2)
    denominator = m.gamma(d/2 + 1)
    # d is the number of dimensions of the sphere 
    return numerator/denominator

#Exc3: numba version
@njit
def sphere_volume_numba(n:int, d:int)->float: # much faster, especially after being run once. After first run the code has been comipled as machine code --> faster execution for second run
    # n is the number of points

    # d is the number of dimensions of the sphere
    #np is the number of processes
        # n is the number of points

    # d is the number of dimensions of the sphere 
    n_c = 0
    for _ in range(n):
        sum_sq = 0
        for _ in range(d):
            x = random.uniform(-1,1)
            sum_sq += x**2
        if sum_sq <= 1:
            n_c += 1

    return (2**d)*n_c/n

#Exc4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel(n, d, np=10):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    n_per_process = n // np
    with future.ProcessPoolExecutor() as executor:
        futures = [executor.submit(sphere_volume, n_per_process, d) for _ in range(np)]
        results = [f.result() for f in futures]
    return sum(results)/np
    
def main():
    # Exc1
    dots = [1000, 10000, 100000]
    for n in dots:
        print(approximate_pi(n))

    # Exc2
    n = 100000
    d = 2
    print(sphere_volume(n, d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    print(sphere_volume(n, d))
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    # Exc3
    run = 1
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start} for run number {run}")

    run += 1
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start} for run number {run}")
    run += 1
    start = pc()
    sphere_volume(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start} for run number {run}")

    print("What is numba time?")
    run = 1
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start} for run number {run}")

    run += 1
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start} for run number {run}")

    run += 1
    start = pc()
    sphere_volume_numba(n, d)
    stop = pc()
    print(f"Exc3: Sequential time of {d} and {n}: {stop-start} for run number {run}")

    # Exc4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume_parallel(n, d)
    stop = pc()
    print(f"Exc4: Sequential time of {d} and {n}: {stop-start}")
    print("What is parallel time?")

    
    

if __name__ == '__main__':
	main()
