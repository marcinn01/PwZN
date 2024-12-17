import numpy as np
import rich
from rich.progress import track
from PIL import Image, ImageDraw
import argparse
import os
import time
import numba

rich.get_console().clear()

parser = argparse.ArgumentParser(description="2D Ising Model Simulation")
parser.add_argument("n", type=int, help="Creating of nxn size lattice")
parser.add_argument("J", type=float, help="Value of J (całka wymiany)")
parser.add_argument("beta", type=float, help="Temperature parameter")
parser.add_argument("B", type=float, help="External magnetic field")
parser.add_argument("steps", type=int, help="Number of steps in the simulation")
parser.add_argument('--positive', '-p', type=float, default=0.5, help='Percentage of positive spins, default=0.5')
parser.add_argument('--animation', '-a', help="Give a name for gif output")
args = parser.parse_args()

n = args.n
J = args.J
beta = args.beta
B = args.B
steps = args.steps
prob = 1 - args.positive

@numba.njit
def initialize(current_state):
    for i in range(n):
        for j in range(n):
            if np.random.rand() < prob:
                current_state[i, j] = -1
            else:
                current_state[i, j] = 1
    return current_state

# M = suma_spinów / liczba_spinów
@numba.njit
def magnetization(current_state):
    return np.sum(current_state) / (n ** 2)

@numba.njit
def hamiltonian(current_state):
    sum1 = 0
    sum2 = 0
    for i in range(n):
        for j in range(n):
            ui = (i + 1)
            uj = (j + 1)
            li = (i - 1 + n)
            lj = (j - 1 + n)

            sum1 += current_state[i, j] * (current_state[i+1, j] + current_state[i-1, j] 
                                            + current_state[i, j+1] + current_state[i, j-1])
            sum2 += current_state[i, j]

    return -J * sum1 - B * sum2

# pojedynczy krok MC - zmiana losowego spinu (algorytm Metropolis)
@numba.njit
def update(current_state):
    for _ in range(n * n):
        E1 = hamiltonian(current_state)
        x, y = np.random.randint(0, n, size=2)
        current_state[x, y] *= -1
        E2 = hamiltonian(current_state)
        deltaE = E2 - E1
        if deltaE > 0 and np.random.rand() > np.exp(-beta * deltaE):
            current_state[x, y] *= -1
    return current_state

def draw_state(current_state):
    img = Image.new('RGB', (n*5, n*5), (0, 0, 0))  
    draw = ImageDraw.Draw(img)
    for i in range(n):
        for j in range(n):
            color = (255, 0, 0) if current_state[j, i] == -1 else (0, 0, 255)  
            draw.rectangle((i * 5, j * 5, i * 5 + 5, j * 5 + 5), color)
    return img

def simulate():
    zero_state = np.ones((n, n), dtype=int)
    images, magnet = [], []
    current_state = initialize(zero_state)
    images.append(draw_state(current_state))
    magnet.append(magnetization(current_state))
    for i in track(range(steps), description="Processing..."):
        current_state = update(current_state)
        images.append(draw_state(current_state))
        magnet.append(magnetization( current_state))
    if args.animation:
        images[0].save(args.animation + '.gif', save_all=True, append_images=images[1:], optimize=False,
                        duration=20 * steps, loop=0)
        
start = time.time()
simulate()

stop = time.time()
print("Time =", stop - start)