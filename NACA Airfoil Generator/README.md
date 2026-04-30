## NACA Airfoil Generator

- `NACA_Airfoil_Generator.exe` can be download and ran directly, no installation needed.
- With it you can generate 4-digit NACA airfoils with ease, and save a `.txt` file of its coordinates.
- It will automatically create a folder to hold your wing files called `NACA_WINGS` in the same place where you store the `.exe`
- The advantage of this program versus ones you can find on the web, is that the output is formatted to be imported directly into SolidWorks with no reformatting necessary.

Within the `source-code` folder you will find the Python program(s) that it runs off of.

# Application Instructions:

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