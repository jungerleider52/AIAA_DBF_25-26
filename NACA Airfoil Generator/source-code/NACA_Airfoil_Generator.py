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
import os
import numpy as np
import math
import tkinter as tk
from tkinter import messagebox

HELP_TEXT = """
4 Digit NACA Airfoil Dimensions Calculator.

Output is formatted to be directly importable to SolidWorks XYZ Curve Feature as a .txt file.

The NACA four-digit wing sections define the profile by:
1) First digit describing maximum camber as percentage of the chord.
2) Second digit describing the distance of maximum camber from the airfoil leading edge in tenths of the chord.
3) Last two digits describing maximum thickness of the airfoil as percent of the chord.

For example, the NACA 2412 airfoil has a maximum camber of 2% located 40% (0.4 chords) from the leading edge with a maximum thickness of 12%.

The NACA 0015 airfoil is symmetrical. The "00" indicates no camber. The "15" indicates a 15% thickness-to-chord ratio.

The maximum thickness is located at 30% of the chord.

From: https://en.wikipedia.org/wiki/NACA_airfoil

Author: Joey Ungerleider
Version: 4-24-26
"""

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
        msg = "NACA code must be an integer."
        #print(msg)
        return None, msg
    if len(code) != 4:
        msg = "NACA code must be 4-digits."
        #print(msg)
        return None, msg
    if chord <= 0:
        msg = "Chord length must be greater than 0."
        #print(msg)
        return None, msg
    
    thickness = int(code[2:]) / 100
    thickness = round(thickness, 2)
    if not 0 < thickness < 1:
        msg = "Thickness must be a value between 0 and 1."
        #print(msg)
        return None, msg
    
    # symmetric airfoil
    if int(code[0]) == 0 and int(code[1]) == 0:
        return symmetric_airfoil(code, chord, thickness, resolution=resolution)

    # cambered airfoil
    camber = int(code[0]) / 100
    camberLocation = int(code[1]) / 10
    if not 0 < camber <= 0.09:
        msg = "Camber must be a value between 0 and 0.09."
        #print(msg)
        return None, msg
    if not 0 < camberLocation <= 0.9:
        msg = "Camber Location must be a value between 0 and 0.9."
        #print(msg)
        return None, msg
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
    os.makedirs("NACA_Wings", exist_ok=True)
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

    #print(f"\n~~ Generated a NACA {code} airfoil; chord length {chord}. Saved to: {filename} ~~\n")
    return filename, f"\n~~ Generated a NACA {code} airfoil; chord length {chord}. Saved to: {filename} ~~\n"

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
    os.makedirs("NACA_Wings", exist_ok=True)
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

    #print(f"\n~~ Generated a NACA {code} airfoil; chord length {chord}. Saved to: {filename} ~~\n")
    return filename, f"\n~~ Generated a NACA {code} airfoil; chord length {chord}. Saved to: {filename} ~~\n"

def get_airfoil_data(filename):
    data = np.loadtxt(filename)
    return data[:, 0], data[:, 1]

def plot_airfoil_2D(filename):
    """
    Plot an airfoil cross section.

    Args:
        filename: name of airfoil file to plot
    """
    # if filename == None:
    #     print("Plot Generation Error: Invalid filename, check airfoil generation.")
    #     return None
    
    # x = []
    # y = []
    # for line in np.loadtxt(filename, delimiter=' '):
    #     x.append(line[0])
    #     y.append(line[1])
    # if len(x) == 0 or len(y) == 0:
    #     print("Plot Generation Error: Empty File.")
    #     return None
    # y_i = [num*(-1) for num in y]

    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.grid()
    # plt.plot(x, y, c='k')
    # plt.show()

class AirfoilGUI:
    def __init__(self, root):
        self.root = root

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.root.minsize(200, 200)
        self.root.geometry("1000x800+50+50")
        self.filename = None

        # inputs
        top_frame = tk.Frame(root, width=1000, height=40, bg="purple")
        top_frame.pack(padx=5, pady=5, side=tk.TOP, fill=tk.Y)
        bot_frame = tk.Frame(root, width=1000, height=40, bg="yellow")
        bot_frame.pack(padx=5, pady=5, side=tk.BOTTOM, fill=tk.Y)
        self.root.title("NACA Airfoil Generator")

        tk.Label(root, text="NACA Code (4 digits):").pack(padx=5, pady=5)
        self.code_entry = tk.Entry(root)
        self.code_entry.insert(0, "2412")
        self.code_entry.pack(padx=5, pady=5)

        tk.Label(root, text="Chord Length:").pack(padx=5, pady=5)
        self.chord_entry = tk.Entry(root)
        self.chord_entry.insert(0, "5")
        self.chord_entry.pack(padx=5, pady=5)

        tk.Label(root, text="Resolution:").pack(padx=5, pady=5)
        self.res_entry = tk.Entry(root)
        self.res_entry.insert(0, "1000")
        self.res_entry.pack(padx=5, pady=5)

        # Buttons
        tk.Button(root, text="Generate Airfoil", command=self.generate).pack(padx=5, pady=5)
        tk.Button(root, text="Plot Airfoil", command=self.plot).pack(padx=5, pady=5)
        tk.Button(self.root, text="Help/Info", command=self.show_help).pack(padx=5, pady=5)
        
        # Output label
        self.output_label = tk.Label(root, text="", fg="blue")
        self.output_label.pack(padx=5, pady=5)

        # Plot
        self.canvas = tk.Canvas(root, width=800, height=300, bg="white")
        self.canvas.pack(padx=20, pady=20)

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help/Info")
        help_window.geometry("1000x500")
        help_window.transient(self.root)
        help_window.grab_set()

        # Frame to hold text + scrollbar
        frame = tk.Frame(help_window)
        frame.pack(fill="both", expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        # Text widget
        text = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
        text.insert("1.0", HELP_TEXT)
        text.config(font=("Segoe UI", 10), state="disabled", padx=10, pady=10)
        tk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=5)
        text.pack(fill="both", expand=True)

        scrollbar.config(command=text.yview)

    def generate(self):
        code = self.code_entry.get()

        try:
            chord = float(self.chord_entry.get())
        except:
            messagebox.showerror("Error", "Chord length must be numerical.")
            return
        try:
            resolution = int(self.res_entry.get())
        except:
            messagebox.showerror("Error", "Resolution must be an integer.")
            return

        filename, msg = airfoil(code, chord, resolution)

        if filename is None:
            messagebox.showerror("Error", msg)
        else:
            self.filename = filename
            self.output_label.config(text=msg)

    def plot(self):
        if self.filename is None:
            messagebox.showwarning("Warning", "Generate airfoil first.")
            return

        x, y = get_airfoil_data(self.filename)

        self.canvas.delete("all")

        # Normalize data to fit canvas
        width = 800
        height = 300

        min_x, max_x = min(x), max(x)
        min_y, max_y = min(y), max(y)

        scale_x = width / (max_x - min_x)
        scale_y = height / (max_y - min_y)

        scale = min(scale_x, scale_y) * 0.9  # padding

        offset_x = 20
        offset_y = height // 2

        points = []
        for xi, yi in zip(x, y):
            px = (xi - min_x) * scale + offset_x
            py = offset_y - yi * scale
            points.append((px, py))

        # Draw lines
        for i in range(len(points) - 1):
            self.canvas.create_line(
                points[i][0], points[i][1],
                points[i+1][0], points[i+1][1],
                fill="black"
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = AirfoilGUI(root)
    root.mainloop()
