import numpy as np
import math
from scipy.interpolate import CubicSpline
from rcg_plot import plot, plot_plain

def pol2cart(rho, phi):
    """
    Convert polar coordinates to cartesian
    """
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def cart2pol(x, y):
    """
    Convert cartesian coordinates to polar
    """
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

# Parameters for random circuit generator 
corners = np.random.randint(12,30) # amount of corners

# Let it loop until it finds a circuit which looks reasonable
while True:
    # Random numbers
    rho_base = np.random.randint(10,20)
    rho_spread = np.random.randint(2,8)

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
        break
    else:
        continue

# Nice plot with statistics and corner labels
plot(x2, y2, df, phis2, distance)

# # Simple plot with just the circuit
# plot_plain(x2, y2, df, phis2, distance)

# Export cicruit coordinates to text file or numpy file
with open('export/circuit.txt', 'w') as f:
    for i in range(len(x2)):
        f.write(str(x2[i])+' '+str(y2[i])+'\n')

with open('export/circuit.npy', 'wb') as f:
    np.save(f, [x2, y2])

# -------------------------------------------------------------------
# To fix/add:
# Add more randomness
# Add main straight -> add pits (graphically)
# Simulate cars?
# Make game out of it
# Add random name
# Possibility of double-circuit -> i.e. 2 parts of track at one phi