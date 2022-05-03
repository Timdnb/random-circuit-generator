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