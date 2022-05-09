import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import interp1d, CubicSpline

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

# Parameters for random circuit generator | all will be random in future
corners = np.random.randint(12,30) # amount of corners
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

    # Straights
    random_split = int(0.75*corners) #np.random.randint(2,len(phis)-2)
    phis = [phis[:random_split-2], phis[random_split+2:]]
    rhos = [rhos[:random_split-2], rhos[random_split+2:]]

    df = []
    x2f, y2f = [], []
    phis2f, rhos2f = np.array([]), np.array([])

    for i in range(len(phis)):
        f = CubicSpline(phis[i], rhos[i], bc_type='clamped')
        df = np.append(df, CubicSpline(phis[i], rhos[i], bc_type='clamped').derivative().roots())
        phis2 = np.linspace(phis[i][0], phis[i][-1], 500)
        rhos2 = f(phis2)
        x2, y2 = pol2cart(rhos2, phis2)
        # Append to arrays
        x2f.append(list(x2))
        y2f.append(list(y2))
        phis2f = np.append(phis2f, phis2)
        rhos2f = np.append(rhos2f, rhos2)

    for i in range(len(y2f)-1):
        dx1 = x2f[i+1][0]-x2f[i][-1]
        dy1 = y2f[i+1][0]-y2f[i][-1]
        dx2 = x2f[i][-1]-x2f[i][-2]
        dy2 = y2f[i][-1]-y2f[i][-2]
        new_point1 = [x2f[i][-1]+0.3*dx1, y2f[i][-1]+0.3*dy1]
        x2f[i].append(new_point1[0])
        y2f[i].append(new_point1[1])
        f = CubicSpline(x2f[i][-2:], y2f[i][-2:], bc_type=((1, dy2/dx2), (1, dy1/dx1)))
        x = np.linspace(x2f[i][-2], x2f[i][-1], 20)
        y = f(x)
        # x2f[i].extend(list(x))
        # y2f[i].extend(list(y))
        x2f[i] = x2f[i][:-1] + list(x)
        y2f[i] = y2f[i][:-1] + list(y)

        dx3 = x2f[i+1][1]-x2f[i+1][0]
        dy3 = y2f[i+1][1]-y2f[i+1][0]
        new_point2 = [x2f[i+1][0]-0.2*dx1, y2f[i+1][0]-0.2*dy1]
        x2f[i+1].insert(0, new_point2[0])
        y2f[i+1].insert(0, new_point2[1])
        f = CubicSpline(x2f[i+1][:2], y2f[i+1][:2], bc_type=((1, dy1/dx1), (1, dy3/dx3)))
        x = np.linspace(x2f[i+1][0], x2f[i+1][1], 20)
        y = f(x)
        # x2f[i+1].insert(0, list(x))
        # y2f[i+1].insert(0, list(y))
        x2f[i+1] = list(x) + x2f[i+1][1:]
        y2f[i+1] = list(y) + y2f[i+1][1:]
    
    x2f = np.array(x2f[0]+x2f[1])
    y2f = np.array(y2f[0]+y2f[1])

    # Filter out weird circuits
    if min(rhos2f) > 0 and max(rhos2f) < 3*rho_base:
        distance = sum(((x2f[i]-x2f[i-1])**2+(y2f[i]-y2f[i-1])**2)**0.5 for i in range(1,len(x2f)))
        print(distance)
        break
    else:
        continue

    # # Interpolation to create smooth circuit
    # f = CubicSpline(phis, rhos, bc_type='clamped')
    # df = CubicSpline(phis, rhos, bc_type='clamped').derivative().roots()
    # phis2 = np.linspace(phis[0], phis[-1], 1000)
    # rhos2 = f(phis2)
    # x, y = pol2cart(rhos, phis)
    # x2, y2 = pol2cart(rhos2, phis2)

    # # Filter out weird circuits
    # if min(rhos2) > 0 and max(rhos2) < 3*rho_base:
    #     distance = sum(((x2[i]-x2[i-1])**2+(y2[i]-y2[i-1])**2)**0.5 for i in range(1,len(x2)))
    #     print(distance)
    #     break
    # else:
    #     continue

# x_test = np.linspace(-10,10,1000)
# y_test = 0*x_test+2
# rho_test, phi_test = cart2pol(x_test, y_test)
# plt.subplot(121)
# # plt.plot(x, y, 'o')
# # plt.plot(x2f[0], y2f[0], 'o')
# # plt.plot(x2f[1], y2f[1], 'o')
# plt.plot(x2f, y2f)
# plt.plot(x_test, y_test)
# plt.subplot(122)
# # plt.plot(phis, rhos, 'o')
# # plt.plot(phis2f, rhos2f, 'o')
# plt.plot(phi_test, rho_test)
# plt.show()

# distance = 1
# x2 = x2f
# y2 = y2f

# -------------------------------------------------------------------
# Fancy plot
# Background color
plt.rcParams['axes.facecolor'] = '#8FCF4C'
# Kerbs, grass and gravel
plt.plot(x2f, y2f, color='darkgreen', linewidth=10)
for j, i in enumerate(df):
    corners = (x2f[np.where(abs(phis2f-i) < 0.1)[0]], y2f[np.where(abs(phis2f-i) < 0.1)[0]])
    plt.plot(corners[0], corners[1], color='grey', linewidth=10)
    plt.plot(corners[0], corners[1], color='white', linewidth=5.5)
    plt.plot(corners[0], corners[1], 'r:', linewidth=5.5)
    # Add corner numbers
    text = False    # make true/false if you (don't) want to see the corner numbers
    if text and len(corners[0]) > 0:
        xtext, ytext = corners[0][int(len(corners[0])/2)], corners[1][int(len(corners[1])/2)]
        rho, phi = cart2pol(xtext, ytext)
        rho += 3
        xtext, ytext = pol2cart(rho, phi)
        plt.text(xtext, ytext, j+1, fontsize=12, color='white')
# Full track
plt.plot(x2f, y2f, color='black', linewidth=4, label=f'length = {round(distance, 2)}')
plt.axis('equal')
plt.legend()
plt.show()

# # -------------------------------------------------------------------
# # Fancy plot
# # Background color
# plt.rcParams['axes.facecolor'] = '#8FCF4C'
# # Kerbs, grass and gravel
# plt.plot(x2, y2, color='darkgreen', linewidth=10)
# for j, i in enumerate(df):
#     corners = (x2[np.where(abs(phis2-i) < 0.1)], y2[np.where(abs(phis2-i) < 0.1)])
#     plt.plot(corners[0], corners[1], color='grey', linewidth=10)
#     plt.plot(corners[0], corners[1], color='white', linewidth=5.5)
#     plt.plot(corners[0], corners[1], 'r:', linewidth=5.5)
#     # Add corner numbers
#     text = False    # make true/false if you (don't) want to see the corner numbers
#     if text and len(corners[0]) > 0:
#         xtext, ytext = corners[0][int(len(corners[0])/2)], corners[1][int(len(corners[1])/2)]
#         rho, phi = cart2pol(xtext, ytext)
#         rho += 3
#         xtext, ytext = pol2cart(rho, phi)
#         plt.text(xtext, ytext, j+1, fontsize=12, color='white')
# # Full track
# plt.plot(x2, y2, color='black', linewidth=4, label=f'length = {round(distance, 2)}')
# plt.axis('equal')
# plt.legend()
# plt.show()

# -------------------------------------------------------------------
# To fix/add:
# Overlapping grey stuff
# Add corner labels?
# Nicer stats label
# Add more randomness
# Add main straight -> add pits
# Simulate cars?
# Make game out of it
# Add random name
# Possibility of double-circuit -> i.e. 2 parts of track at one phi

# Steps to add straight
# split the points into x amount of sections
# apply cubic splines to each section, specify boundary condition where slope is equal to slope between points
# connect them all together

# tijdelijk:
# if i < len(phis)-1:
        #     x = rhos[i][0]*np.cos(phis[i][0])
        #     y = rhos[i][0]*np.sin(phis[i][0])
        #     dx = rhos[i+1][-1]*np.cos(phis[i+1][-1])-rhos[i][-1]*np.cos(phis[i][-1])
        #     dy = rhos[i+1][-1]*np.sin(phis[i+1][-1])-rhos[i][-1]*np.sin(phis[i][-1])
        #     dr = np.cos(phis[i][0])*dx+np.sin(phis[i][0])*dy
        #     dphi = (x*dy-y*dx)/(x**2+y**2)
        #     drdphi = dr/dphi
        #     print(drdphi)

        #     r1 = rhos[i][-1]
        #     r2 = rhos[i+1][0]
        #     phi1 = phis[i][-1]
        #     phi2 = phis[i+1][0]
        #     dr = r2-r1
        #     dphi = phi2-phi1
        #     drdphi = dr/dphi
        #     print(drdphi)
            
        #     dx = rhos[i+1][-1]*np.cos(phis[i+1][-1])-rhos[i][-1]*np.cos(phis[i][-1])
        #     dy = rhos[i+1][-1]*np.sin(phis[i+1][-1])-rhos[i][-1]*np.sin(phis[i][-1])
        #     r = rhos[i][-1]
        #     phi = phis[i][-1]

        #     drdphi = ((dy/dx)*r*np.sin(phi)+r*np.cos(phi))/((dy/dx)*np.cos(phi)-np.sin(phi))
        #     print(drdphi)
        # if i % 2 == 0:
        #     f = CubicSpline(phis[i], rhos[i], bc_type=((1, 0.0), (1, drdphi))) # add correct bcs
        #     df = np.append(df, CubicSpline(phis[i], rhos[i], bc_type=((1, 0.0), (1, drdphi))).derivative().roots())
        # else:
        #     f = CubicSpline(phis[i], rhos[i], bc_type=((1, -drdphi), (1, 0.0))) # add correct bcs
        #     df = np.append(df, CubicSpline(phis[i], rhos[i], bc_type=((1, -drdphi), (1, 0.0))).derivative().roots())
