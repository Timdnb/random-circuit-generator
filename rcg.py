import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d, CubicSpline

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

# Parameters for random circuit generator | all will be random in future
corners = np.random.randint(12,20) # amount of corners
i =0
while True:
    # Random numbers
    rho_base = np.random.randint(12,15)
    rho_spread = np.random.randint(4,8)

    # Create points
    phis = np.sort(np.random.rand(corners)*2*math.pi)
    rhos = np.random.rand(corners)*rho_spread+rho_base

    # Elongate circuit
    rhos = np.where(phis < math.pi/3, 2*rhos, rhos)
    rhos = np.where(abs(phis-math.pi) < math.pi/3, 2*rhos, rhos)
    rhos = np.where(abs(phis-2*math.pi) < math.pi/3, 2*rhos, rhos)

    # Connect points in a loop
    phis = np.append(phis, phis[0]+2*math.pi)
    rhos = np.append(rhos, rhos[0])

    # Interpolation to create smooth circuit
    f = CubicSpline(phis, rhos, bc_type='clamped')
    df = CubicSpline(phis, rhos, bc_type='clamped').derivative().roots()
    phis2 = np.linspace(phis[0], phis[-1], 1000)
    rhos2 = f(phis2)
    x, y = pol2cart(rhos, phis)
    x2, y2 = pol2cart(rhos2, phis2)

    # Filter out weird circuits
    if min(rhos2) > 0 and max(rhos2) < 3*rho_base:
        distance = sum(((x2[i]-x2[i-1])**2+(y2[i]-y2[i-1])**2)**0.5 for i in range(1,len(x2)))
        print(distance)
        break
    else:
        continue

# Fancy plot
plt.rcParams['axes.facecolor'] = '#8FCF4C'
plt.plot(x2, y2, color='darkgreen', linewidth=10)
for i in df:
    corners = (x2[np.where(abs(phis2-i) < 0.1)], y2[np.where(abs(phis2-i) < 0.1)])
    plt.plot(corners[0], corners[1], color='grey', linewidth=10)
    plt.plot(corners[0], corners[1], color='white', linewidth=5.5)
    plt.plot(corners[0], corners[1], 'r:', linewidth=5.5)
plt.plot(x2, y2, color='black', linewidth=4, label=f'length = {round(distance, 2)}')
plt.axis('equal')
plt.legend()
plt.show()

# V1
import numpy as np
import matplotlib.pyplot as plt
import math

# Parameters for random circuit generator | all will be random in future
length = 10                 # total circuit length
drs_sections = 2            # amount of drs sections
corners = 1000                # amount of corners
main_straight = 1           # length of main straight
height_differences = False  # if True, height differences will be present

more = True

# Create points
points = np.random.rand(corners-2, 2)*2-1
while more:
    points = points[np.where(np.logical_or(np.arctan2(points[:,1], points[:,0]) > -2*math.pi/6, np.arctan2(points[:,1], points[:,0]) < -4*math.pi/6))]
    if len(points) < corners-2:
        points = np.append(points, np.random.rand(corners-len(points), 2)*2-1, axis=0)
    else:
        more = False
# Add two points for main straight
y = -0.5
points = np.append(points, np.array([[0, 0], [0, 0]]), axis=0)

# Put points in circuit order
plt.plot(points[:,0], points[:,1], 'o')
plt.show()

# V2
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# Parameters for random circuit generator | all will be random in future
length = 10                 # total circuit length
corners = 21              # amount of corners
height_differences = False  # if True, height differences will be present

# Create points and put in order
points = np.random.rand(corners, 2)*2-1
angs = np.sort(np.arctan2(points[:,1], points[:,0]))
points_new = []
for ind in range(len(points)):
    for i in range(len(points)):
        if (np.arctan2(points[i,1], points[i,0])) == angs[ind]:
            points_new.append(points[i])
        else:
            continue
points_new.append(points_new[0])
points_new = np.array(points_new)

# Switcg a few points
for j in range(int(corners/7)):
    i = np.random.randint(0, corners)
    if np.random.randint(0,2) == 1:
        a = points_new[i]
        points_new[i] = points_new[i+1]
        points_new[i+1] = a

Path = mpath.Path

fig, ax = plt.subplots()
for i in range(1, len(points)-1, 2):
    pp1 = mpatches.PathPatch(
        Path([points_new[i-1], points_new[i], points_new[i+1]],
            [Path.MOVETO, Path.CURVE3, Path.CURVE3]),
        fc="none", transform=ax.transData)
    ax.add_patch(pp1)


# Put points in circuit order
ax.plot(points_new[:,0], points_new[:,1])
plt.show()

# V3
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)+math.pi
    return(phi, rho)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

# Parameters for random circuit generator | all will be random in future
length = 10                 # total circuit length
corners = 21              # amount of corners
height_differences = False  # if True, height differences will be present

# Create points and put in order
points = np.random.rand(corners, 2)*2-1
angs = np.sort(np.arctan2(points[:,1], points[:,0]))
points_new = []
for ind in range(len(points)):
    for i in range(len(points)):
        if (np.arctan2(points[i,1], points[i,0])) == angs[ind]:
            points_new.append(points[i])
        else:
            continue
# points_new.append(points_new[0])
points_new = np.array(points_new)

# # Switch a few points
# for j in range(int(corners/7)):
#     i = np.random.randint(0, corners)
#     if np.random.randint(0,2) == 1:
#         a = points_new[i]
#         points_new[i] = points_new[i+1]
#         points_new[i+1] = a

# To r,theta
rt = cart2pol(points_new[:,0], points_new[:,1])
f2 = interp1d(rt[0], rt[1], kind='cubic')
phis = np.linspace(rt[0][0], rt[0][-1], 10000)
rhos = f2(phis)
xy = pol2cart(rhos, phis)

plt.plot(rt[0], rt[1])
plt.plot(phis, f2(phis))
# plt.plot(points_new[:,0], points_new[:,1], 'o')
# plt.plot(xy[0], xy[1])
plt.show()

