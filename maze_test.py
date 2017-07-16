import numpy as np

from mpgaa import Turtle
import time


x_max, y_max, z_max = 20,10,1

maze = np.ones((x_max,y_max,z_max), dtype=float)

for i in range(x_max):
    for j in range(y_max):
        for k in range(z_max):
            if i == 3 and j < 7:
                maze[(i,j,k)] = np.inf
            if i == 5 and j > 4:
                maze[(i,j,k)] = np.inf
            if i == 7 and j < 7:
                maze[(i,j,k)] = np.inf
            if i == 10 and j > 2:
                maze[(i,j,k)] = np.inf
            if i == 15 and j != 5:
                maze[(i,j,k)] = np.inf
            if 12<=i<15 and j == 6:
                maze[(i,j,k)] = np.inf
            if 12<=i<15 and j == 4:
                maze[(i,j,k)] = np.inf
            pass


start = (0,0,0)
goal = (19,9,0)


x = Turtle(maze, start, goal)


x.Main()


H = x.history
# time.sleep(5)
for x,y,z in H:
    s = []
    s.append('█' * (y_max + 2) + '\n')
    for i in range(x_max):
        s.append('█')
        for j in range(y_max):
            if i == x and j == y:
                s.append('X')
            elif maze[(i,j,0)] == np.inf:
                s.append('█')
            elif i == goal[0] and j == goal[1]:
                s.append('E')
            elif i == start[0] and j == start[1]:
                s.append('S')
            else:
                s.append(' ')
        s.append('█\n')
    s.append('█' * (y_max + 2) + '\n')
    print ''.join(s)
    time.sleep(0.5)
