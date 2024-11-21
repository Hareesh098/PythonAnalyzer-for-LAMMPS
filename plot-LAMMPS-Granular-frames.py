#!/mt/data-fielding/hcharan/Insatalled-Software/anaconda3/bin/python
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
import numpy as np
import sys
from pylab import *
from decimal import Decimal, getcontext
from matplotlib.cm import get_cmap  # Import get_cmap for colormap
from decimal import Decimal, getcontext
# Set the precision high enough
getcontext().prec = 10
from datetime import datetime
import matplotlib.ticker as mtick
# Ensure LaTeX is properly set up
import matplotlib.pyplot as plt
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"



# Check the correct number of arguments
if len(sys.argv) != 4:
    print("Error occurred")
    print("Usage: ./plot-LAMMPS-Granular-frames.py filename.dat skip_header max_rows")
    exit()

# Read the arguments from command line
filename = sys.argv[1]

# Initialize the figure for plotting
fig = figure(1)
ax = fig.add_subplot(111)
ax.set_aspect('equal')

# Set initial y offset for plotting multiple frames
y_offset = 1
frame_height = 4.0  # Height for each frame along the y-axis

headeroffset0 = int(sys.argv[2])
rowoffset0 = int(sys.argv[3])

# Define the colormap
cmap = get_cmap('rainbow')  # Ensure this is defined

# To accumulate all atomIDs for global limits and matrix creation
x_frame_1 = None
fy_matrix = []  # List to store fy values for each frame

# Loop over multiple frames
for i in range(1, 500):  # Adjust as needed
    headerSkip = i * headeroffset0 + (i - 1) * rowoffset0
    
    # Load the data
    data = genfromtxt(filename, skip_header=headerSkip, max_rows=rowoffset0)
    
    if data.size == 0:
        print(f"Warning: No data read for frame {i}. Skipping.")
        continue
    
    # Extract data columns
    atomID = data[:, 0]
    atomRadius = data[:, 1] * 1
    x = data[:, 2]  # x represents the positions of the discs
    y = data[:, 3] + y_offset  # Shift the y positions by the y_offset for the current frame
    vx = data[:, 4]
    vy = data[:, 5]
    fx = data[:, 6]
    fy = data[:, 6]  # Force in y-direction
    
    # Save x-locations from frame i = 1
    if i == 1:
        x_frame_1 = x.copy()  # Copy the x-locations for frame 1
    else:
        x = x_frame_1  # Reuse x-locations from frame 1 for all other frames

    # Append fy values to matrix
    fy_matrix.append(fy)

    # Prepare to plot this frame as a horizontal strip using x as x-axis
    patches = []
    for x1, y1, radius in zip(x, y, atomRadius):
        circle = Circle((x1, y1), radius)
        patches.append(circle)
    
    # Create a PatchCollection for this frame
    colors = fy  # Use fy as color
    p = PatchCollection(patches, alpha=0.4, cmap=cmap, edgecolor='none')  # cmap is now properly defined
    p.set_array(np.array(colors))
    
    # Add the collection to the plot
    ax.add_collection(p)
    #scatter(x,y,c=fy,s=atomRadius*5)
    #Move the y_offset down for the next frame
    y_offset += frame_height

# Set the global limits of the x-axis and y-axis
if x_frame_1 is not None:
    ax.set_xlim([min(x_frame_1), max(x_frame_1)])  # Set x-limits based on the fixed x positions
    ax.set_ylim([0, y_offset])

# Add the colorbar
colorbar = fig.colorbar(p, ax=ax)
colorbar.set_label('Force in Y-Direction (fy)', fontsize=15)

# Add labels and title
ax.set_xlabel('Disc Position (x)')
ax.set_ylabel('Time frames')
plt.title('Progressive Plot of Time Frames (Fixed x Positions)')

# Save the figure and show
plt.tight_layout()
plt.savefig("Progressive_Frames_Fixed_x_Positions.pdf")
plt.show()

# Convert the fy_matrix list to a NumPy array for saving
fy_matrix = np.array(fy_matrix)  # Transpose so rows correspond to discs and columns to time frames

# Save the fy_matrix as a CSV file
np.savetxt("../data/fy_matrix.csv", fy_matrix, delimiter=",")

# Save the matrix as a .npy file (binary format, efficient for large arrays)
np.save("../data/fy_matrix.npy", fy_matrix)

