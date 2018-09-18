import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import math
import random
import copy
np.set_printoptions(precision=3, suppress=True)

# ------------------------------------------------------------------------
# FUNCTIONS TO FIND OPTIMA FOR
def rastrigin(*x):
    return 20 + sum([(i**2 - 10*np.cos(2*math.pi*i)) for i in x])

def squared(x, y):
    return ((x)**2) + ((y)**2)

# ------------------------------------------------------------------------
# DEFINE A PARTICLE CLASS
class particle:
    def __init__(self):
        random.seed()
        self.position = [random.uniform(-4,4) for i in range(2)]
        self.velocity = [random.uniform(-8,8) for i in range(2)]
        # self.error = rastrigin(self.position[0], self.position[1])
        self.error = squared(self.position[0], self.position[1])
        self.SB_position = self.position
        self.SB_error = self.error

# ------------------------------------------------------------------------
# FUNCTION TO FIND THE BEST PARTICLE OF THE SWARM
def swarmBest(swarm, N):
    SwB_error = min([swarm[i].SB_error for i in range(N)])  # Calc the best swarm error
    for i in range(N):
        if swarm[i].SB_error == SwB_error:
            SwB_position = swarm[i].position    # Find particle with best swarm position
    return SwB_position, SwB_error

# ------------------------------------------------------------------------
# SOLVING FUNCTION
def solve(max_its, N):
    random.seed(0)
    swarm = [particle() for n in range(N)]      # Generate swarm of N particles
    SwB_position, SwB_error = swarmBest(swarm, N)     # Calc the best swarm position

    # Plot initial positions
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for p in swarm:
        plt.plot(p.SB_position[0], p.SB_position[1], '.')
        ax.set_xlim([-5,5])
        ax.set_ylim([-5,5])
    # plt.show()

    S_hist = [[] for i in range(N)]
    it = 0
    while it < max_its:
        # print(it)
        for P in range(N):
            temp = copy.copy(swarm[P].position)
            temp.append(swarm[P].error)
            # print(temp)
            S_hist[P].append(temp)

        for i in range(N):      # Loop through particles
            for j in range(2):      # Loop through number of dimensions
                r1 = random.random()
                r2 = random.random()

                # Calc new velocity of particle as weighted sum of its current
                # direction, its current best position, and the swarm best position
                swarm[i].velocity[j] = (w*swarm[i].velocity[j]) + \
                (c1*r1*(swarm[i].SB_position[j] - swarm[i].position[j])) + \
                (c2*r2*(SwB_position[j] - swarm[i].position[j]))

            for k in range(2):      # Update particle position
                swarm[i].position[k] = swarm[i].position[k] + swarm[i].velocity[k]

            # swarm[i].error = rastrigin(swarm[i].position[0], swarm[i].position[1])
            swarm[i].error = squared(swarm[i].position[0], swarm[i].position[1])


            if swarm[i].error < swarm[i].SB_error:
                    swarm[i].SB_position = swarm[i].position
                    swarm[i].SB_error = swarm[i].error

                    if swarm[i].SB_error < SwB_error:
                        SwB_position, SwB_error = swarmBest(swarm, N)

        if it%10 == 0:
            print('Iteration: ', it, '  ||  Best Error:', SwB_error)
        it += 1

    print('\n\nBEST SOLUTION')
    print('x-value:', SwB_position[0], '\ny-value:', SwB_position[1], '\nError:', SwB_error)
    for part in S_hist:
        X = [i[0] for i in part]
        Y = [i[1] for i in part]
        plt.plot(X,Y,)
    return S_hist

# ------------------------------------------------------------------------
# SETUP UP AND RUN SOLVER
if __name__ == '__main__':
    w = 0.32
    c1 = 0.54
    c2 = 0.1
    N = 100
    num_its = 100
    random.seed(0)
    print('PARTICLE SWARM OPTIMISATION', '\nMax number of iterations: ', num_its, '\nNumber of particles: ', N)

    S_hist = solve(num_its, N)

    x = np.linspace(-5,5,120)
    y = np.linspace(-5,5,120)
    xx, yy = np.meshgrid(x, y)
    # zz = rastrigin(xx,yy)
    zz = squared(xx,yy)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=True)
    for part in S_hist:
        X = [i[0] for i in part]
        Y = [i[1] for i in part]
        Z = [i[2] for i in part]
        ax.plot(X,Y,Z)
    plt.show()
