"""4 Digit NACA Airfoil Dimensions Calculator.

Output is formatted to be directly importable to SolidWorks XYZ Curve Feature as a .txt file.

The NACA four-digit wing sections define the profile by:
1) First digit describing maximum camber as percentage of the chord.
2) Second digit describing the distance of maximum camber from the airfoil leading edge in tenths of the chord.
3) Last two digits describing maximum thickness of the airfoil as percent of the chord.

For example, the NACA 2412 airfoil has a maximum camber of 2% located 40% (0.4 chords) from the leading edge with a maximum thickness of 12% of the chord.
The NACA 0015 airfoil is symmetrical, the 00 indicating that it has no camber. The 15 indicates that the airfoil has a 15% thickness to chord length ratio: it is 15% as thick as it is long.

The maximum thickness of the four-digit series is always located at 30% of the chord.

From: https://en.wikipedia.org/wiki/NACA_airfoil

Author: Joey Ungerleider
Version: 11-21-24
"""
import numpy as np
import math
import matplotlib.pyplot as plt

def airfoil(code, chord, resolution=1000):
    """
    Generate a curve for a NACA airfoil and save it to a file.

    Args:
        code: 4-digit NACA code to generate
        chord: chord length in whatever units your CAD software will use
        resolution: number of x-points, 1000-3000 recommended
    Return:
        filename: local filename to save the dims to
    
    """
    try:
        intCode = int(code)
    except:
        print("NACA Code Error: NACA code must be an integer.")
        return None
    if len(code) != 4:
        print("NACA Code Error: NACA code must be 4-digits.")
        print(len(code))
        return None
    if chord <= 0:
        print("Airfoil Generation Error: Chord length must be greater than 0")
        return None
    
    thickness = int(str(code[2]) + str(code[3])) / 100
    thickness = round(thickness, 2)
    if not 0 < thickness < 1:
        print("Airfoil Generation Error: Thickness must be a value between 0 and 1")
        return None
    
    # symmetric airfoil
    if int(code[0]) == 0 and int(code[1]) == 0:
        return symmetric_airfoil(code, chord, thickness, resolution=resolution)

    # cambered airfoil
    camber = int(code[0]) / 100
    camberLocation = int(code[1]) / 10
    if not 0 < camber <= 0.09:
        print("Airfoil Generation Error: Camber must be a value between 0 and 0.09")
        return None
    if not 0 < camberLocation <= 0.9:
        print("Airfoil Generation Error: Camber Location must be a value between 0 and 0.9")
        return None
    return cambered_airfoil(intCode, chord, thickness, camber, camberLocation, resolution=resolution)

def symmetric_airfoil(code, chord, thickness, resolution=1000):
    """
    Generate a curve for a symmetrical NACA airfoil

    Args:
        chord: desired chord length of the wing
        thickness: percent of chord length, max thickness of the wing
    Return:
        filename: local filename to save the dims to
    """
    # calculate n position points from 0 to 1.0
    x = np.linspace(start=0, stop=1, num=resolution)
    U = []
    L = []

    # generate half-thickness values at a given x position (centerline to outer edge)
    filename = f"NACA-{code}_CHORD-{chord}"
    filename = 'NACA_Wings/' + filename + '.txt'
    with open(filename, 'w') as file:
        for i, p in enumerate(x):
            yt = 5*thickness*(0.2969*math.sqrt(p) - 0.126*p - 0.3516*p**2 + 0.2843*p**3 - 0.1015*p**4)
            x_actual = p * chord
            y_actual = yt * chord

            U.append(f"{x_actual} {y_actual} 0\n")
            L.append(f"{x_actual} {-1*y_actual} 0\n")
        
        L.reverse()
        for i in range(len(U) - 1):
            file.write(U[i])
        for i in range(len(L)):
            file.write(L[i])

    print(f"\n~~ Generated a NACA {code} airfoil; chord length {chord}. Saved to: {filename} ~~\n")
    return filename

def cambered_airfoil(code, chord, thickness, camber, camberLocation, resolution=1000):
    """
    Generate a curve for a cambered NACA airfoil

    Args:
        chord: desired chord length of the wing
        thickness: percent of chord length, max thickness of the wing
        filename: local filename to save the dims to
    """
    # calculate n position points from 0 to 1.0
    x = np.linspace(start=0, stop=1, num=resolution)
    U = []
    L = []

    # generate half-thickness values at a given x position (centerline to outer edge)
    filename = f"NACA-{code}_CHORD-{chord}"
    filename = 'NACA_Wings/' + filename + '.txt'
    with open(filename, 'w') as file:
        for i, p in enumerate(x):
            yt = 5*thickness*(0.2969*math.sqrt(p) - 0.126*p - 0.3516*p**2 + 0.2843*p**3 - 0.1036*p**4)
            if 0 <= p <= camberLocation:
                yc = (camber / camberLocation**2) * (2*camberLocation*p - p**2)
                dydx = (2*camber / camberLocation**2) * (camberLocation - p)
            else:
                yc = (camber / (1-camberLocation)**2) * ((1 - 2*camberLocation) + 2*camberLocation*p - p**2)
                dydx = (2*camber / (1 - camberLocation**2)) * (camberLocation - p)
            
            theta = math.atan(dydx)
            xU = (p - yt*math.sin(theta)) * chord
            yU = (yc + yt*math.cos(theta)) * chord
            xL = (p + yt*math.sin(theta)) * chord
            yL = (yc - yt*math.cos(theta)) * chord

            U.append(f"{xU} {yU} 0\n")
            L.append(f"{xL} {yL} 0\n")
        L.reverse()
        for i in range(len(U) - 1):
            file.write(U[i])
        for i in range(len(L)):
            file.write(L[i])

    print(f"\n~~ Generated a NACA {code} airfoil; chord length {chord}. Saved to: {filename} ~~\n")
    return filename

def plot_airfoil_2D(filename):
    """
    Plot an airfoil cross section.

    Args:
        filename: name of airfoil file to plot
    """
    if filename == None:
        print("Plot Generation Error: Invalid filename, check airfoil generation.")
        return None
    
    x = []
    y = []
    for line in np.loadtxt(filename, delimiter=' '):
        x.append(line[0])
        y.append(line[1])
    if len(x) == 0 or len(y) == 0:
        print("Plot Generation Error: Empty File.")
        return None
    y_i = [num*(-1) for num in y]

    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()
    plt.plot(x, y, c='k')
    #plt.plot(x, y_i, c='k')
    plt.show()

if __name__ == "__main__":
    airfoil = airfoil("0012", 5)
    plot_airfoil_2D(airfoil)
