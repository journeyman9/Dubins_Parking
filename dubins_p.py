import dubins
import matplotlib.pyplot as plt
import numpy as np

q0 = [4.2, 4.1, np.pi]
qg = [0, 0, 3*np.pi/4]

turning_radius = 1.0
step_size = 0.5

q1 = qg.copy()
q1[0] -= turning_radius * np.cos(q1[2])
q1[1] -= turning_radius * np.sin(q1[2])

path = dubins.shortest_path(q0, q1, turning_radius)
qs, _ = path.sample_many(step_size)
qs = np.array(qs)

s = np.sqrt((qg[0] - q1[0]) ** 2 + (qg[1] - q1[1]) **2)
n_steps = int(s // step_size) + 1
straight = np.array([np.linspace(q1[0], qg[0], n_steps), 
                    np.linspace(q1[1], qg[1], n_steps), 
                    qg[2] * np.ones(n_steps)]).T
qs = np.vstack((qs, straight))

plt.plot(qs[:, 0], qs[:, 1])
plt.quiver(qs[:, 0], qs[:, 1], np.cos(qs[:, 2]), np.sin(qs[:, 2]), 0.5)
plt.plot(qg[0], qg[1], 'x')
plt.axis('equal')
plt.xlabel('Position in x [m]')
plt.ylabel('Position in y [m]')
plt.show()
