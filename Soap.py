import numpy as np
import matplotlib.pyplot as plt

theta = np.linspace(0, 2 * np.pi, 100) 
z = np.linspace(-1,1,100)
theta, z = np.meshgrid(theta, z)
y0 = 1
x0 = 0
r = y0*np.cosh((z-x0)/y0)

x = r * np.cos(theta)
y = r * np.sin(theta)

fig = plt.figure(dpi = 500)
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(x, y, z)

ax.set_title('Plot of surface area for soap-bubble problem')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')
ax.tick_params(axis='x', pad=40)
ax.tick_params(axis='y', pad=40)
ax.tick_params(axis='z', pad=40)

plt.show()
