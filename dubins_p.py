import dubins
import matplotlib.pyplot as plt
import numpy as np

def distance(a, b):
    return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def get_menger_curvature(a, b, c):
    ''' method to get curvature from three points '''
    raw_area = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    triangle_area = raw_area / 2.0

    return 4 * triangle_area / (distance(a, b) * distance(b, c) * distance(c, a))

## Randomize starting and goal poses
x0 = np.random.randint(-200, 200)
y0 = np.random.randint(-200, 200)
psi_0 = np.radians(np.random.randint(0, 360))

x1 = np.random.randint(-200, 200)
y1 = np.random.randint(-200, 200)
psi_1 = np.radians(np.random.randint(0, 360))

#q0 = [x0, y0, psi_0]
#qg = [x1, y1, psi_1]
q0 = [200, 200, np.pi]
qg = [0, 0, np.pi]

turning_radius = 13.176
step_size = 0.05

## Modify dubins to work for a straight offset from goal
q1 = qg.copy()
q1[0] -= 2 * turning_radius * np.cos(q1[2])
q1[1] -= 2 * turning_radius * np.sin(q1[2])

# Dubins
path = dubins.shortest_path(q0, q1, turning_radius)
qs, dist_dubins = path.sample_many(step_size)
qs = np.array(qs)

## Concatenate with reverse straight
s_s = distance((q1[0], q1[1]), (qg[0], qg[1]))
n_steps = int(s_s // step_size) + 1
straight = np.array([np.linspace(q1[0], qg[0], n_steps), 
                    np.linspace(q1[1], qg[1], n_steps), 
                    qg[2] * np.ones(n_steps)]).T
qs = np.vstack((qs, straight))

dist_straight = [dist_dubins[-1]]
for j in range(len(straight)):
    dist_straight.append(dist_straight[j] + (s_s / n_steps))
dist = dist_dubins + dist_straight[1:] # ignore double counting

## Plots
plt.plot(qs[:, 0], qs[:, 1])
plt.quiver(qs[:, 0], qs[:, 1], np.cos(qs[:, 2]), np.sin(qs[:, 2]), 0.5)
plt.plot(qg[0], qg[1], 'x')
plt.axis('equal')
plt.xlabel('Position in x [m]')
plt.ylabel('Position in y [m]')
plt.show()

## x, y, curv, psi, dist
curv = []
for n in range(len(qs)):
    if n == 0:
        curv.append(get_menger_curvature(qs[0], qs[n+1], qs[n+2]))
    elif n == len(qs) - 1:
        curv.append(get_menger_curvature(qs[n-2], qs[n-1], qs[n]))
    else:
        curv.append(get_menger_curvature(qs[n-1], qs[n], qs[n+1]))

x = qs[:, 0]
y = qs[:, 1]
psi = qs[:, 2]

#plt.plot(dist, curv)
#plt.title('Curvature as a fxn of dist')
#plt.show()
#
#plt.plot(dist, psi)
#plt.title('Heading as a fxn of dist')
#plt.show()
#
#plt.plot(range(len(dist)), dist)
#plt.title('distance as a fxn of index')
#plt.show()

## Plot again to make sure
#plt.plot(x, y)
#plt.quiver(x, y, np.cos(psi), np.sin(psi), 0.5)
#plt.plot(qg[0], qg[1], 'x')
#plt.axis('equal')
#plt.xlabel('Position in x [m]')
#plt.ylabel('Position in y [m]')
#plt.show()

for i in range(len(qs)):
     print(str(x[i]) + ',' + str(y[i]) + ',' + str(curv[i]) + ',' + 
           str(psi[i]) + ',' + str(dist[i]))
