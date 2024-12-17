import numpy as np
import rich
from rich.progress import track
from PIL import Image, ImageDraw
import argparse
import os
import time

rich.get_console().clear()

parser = argparse.ArgumentParser(description="2D Ising Model Simulation")
parser.add_argument("n", type=int, help="Creating of nxn size lattice")
parser.add_argument("J", type=float, help="Value of J (całka wymiany)")
parser.add_argument("beta", type=float, help="Temperature parameter")
parser.add_argument("B", type=float, help="External magnetic field")
parser.add_argument("steps", type=int, help="Number of steps in the simulation")
parser.add_argument('--positive', '-p', type=float, default=0.5, help='Percentage of positive spins, default=0.5')
parser.add_argument('--animation', '-a', help="Give a name for gif output")
parser.add_argument('--save_pictures', '-s', help="Give name for saving pictures")
parser.add_argument('--magnetization', '-m', help="Give name to save file with magnetization values")
args = parser.parse_args()

n = args.n
J = args.J
beta = args.beta
B = args.B
steps = args.steps


prob = 1 - args.positive

class Ising:
    def __init__(self):
        self.state = np.ones((n, n), dtype=int)

    def initialize(self):
        self.state = np.random.choice([-1, 1], size=(n, n), p=[prob, 1 - prob])

    # M = suma_spinów / liczba_spinów
    def magnetization(self, iter):
        magn = np.sum(self.state) / (n ** 2)
        return magn, iter

    # H = -J * sum(s_i * s_j) - B * sum(s_i)
    def hamiltonian(self):
        sum1 = np.sum(self.state * 
            (np.roll(self.state, shift=1, axis=0) +
                np.roll(self.state, shift=-1, axis=0) +
                np.roll(self.state, shift=1, axis=1) +
                np.roll(self.state, shift=-1, axis=1)
            )
        )
        sum2 = np.sum(self.state)
        H = -J * sum1 - B * sum2
        return H

    # pojedynczy krok MC - zmiana losowego spinu (algorytm Metropolis)
    def update(self):
        for _ in range(n ** 2):
            E1 = self.hamiltonian()
            x, y = np.random.randint(0, n, size=2)
            self.state[x, y] *= -1
            E2 = self.hamiltonian()
            deltaE = E2 - E1
            if deltaE > 0 and np.random.rand() > np.exp(-beta * deltaE):
                self.state[x, y] *= -1

    def draw_state(self, iter):
        img = Image.new('RGB', (n, n), (0, 0, 0))  
        draw = ImageDraw.Draw(img)
        for i in range(n):
            for j in range(n):
                color = (255, 0, 0) if self.state[j, i] == -1 else (0, 0, 255)  
                draw.rectangle((i * 5, j * 5, i * 5 + 5, j * 5 + 5), color)
        if args.save_pictures:
            my_name = f"{args.save_pictures}{iter}.png"
            img.save(my_name)
        return img

    def simulate(self):
        images, magnet = [], []
        self.initialize()
        images.append(self.draw_state(0))
        magnet.append(self.magnetization(0))
        for i in track(range(steps), description="Processing..."):
            self.update()
            images.append(self.draw_state(i + 1))
            magnet.append(self.magnetization(i + 1))
        if args.animation:
            images[0].save(args.animation + '.gif', save_all=True, append_images=images[1:], optimize=False,
                           duration=20 * steps, loop=0)
            
            for i in range(steps + 1):
                image_path = f"{args.save_pictures}{i}.png"

        if args.magnetization:
            with open(args.magnetization + '.txt', 'w') as f:
                f.write('n \t magnetization \n')
                for m in magnet:
                    f.write(f"{m[1]}\t{m[0]}\n")

start = time.time()

s1 = Ising()
s1.simulate()


stop = time.time()
print("Time =", stop - start)