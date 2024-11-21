from pylab import *
from datetime import datetime
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt
from matplotlib import cm

# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

DirPath = f"../data/"
FileName = f"xMatrix.dat"
InputMatrixFile = DirPath + FileName
data = np.loadtxt(InputMatrixFile)
data = data.T  # Transpose so that the time increases in column
deltaT = 0.001
frames = 1014
MyEvery = 1e4
time = arange(1, frames + 1)
time = time * deltaT * MyEvery
NgrainsStart = 107
NgrainsEnd = 117
NgrainsDelta = 1
atomID = arange(NgrainsStart, NgrainsEnd, 1)

# Colorbar Flags
colorbarFlag = 1
# Define colormap for color coding based on initial value
cmap = get_cmap('rainbow')
data_at_t0 = data[0, NgrainsStart:NgrainsEnd]
norm = Normalize(vmin=min(data_at_t0), vmax=max(data_at_t0))

# Loading the Cx coordinates so that we get the block's discs' coordinates in
# the block frame of reference
COMdata = np.loadtxt("../data/COM-nAtom130304-Z5.9894-Fy0.0001-Fx6e-05.dat")
T = COMdata[:, 0]
Cx = COMdata[:, 1]
Vx = gradient(Cx, T)
# Extract every 100th line, starting from index 0 (i.e., indices 0, 101, 201, ...)
T_subset = T[::100]
Cx_subset = Cx[::100]
Vx_subset = Vx[::100]

# Fy values
Fy = 0.0001
j = 0
fig, (ax1, ax2) = subplots(2, 1, figsize=(6.4, 9.6))  # Create a figure with two rows of subplots

# Initialize current offset to zero
current_offset = 0

# Plotting x vs time in the first subplot with color coding based on initial value
for i in range(NgrainsStart, NgrainsEnd, NgrainsDelta):
    x = data[:, i]
    x = x - Cx_subset  # Align with the center of mass
    deviation_from_initial = x - x[0]

    # Shift x by the current offset
    x = x - x[0] + current_offset

    # Update the offset for the next plot based on the current plot
    offset_increment = max(x) - min(x)
    current_offset += offset_increment

    # Define the colormap
    cmap = get_cmap('rainbow')  # rainbow=>best #brg=>2nd best #viridis=>3rd best
    norm = Normalize(vmin=-0.05, vmax=0.05)

    # Plot each line segment with color coding based on the value of y
    for j in range(len(x) - 1):
        ax1.plot(time[j:j + 2] * Fy, x[j:j + 2], color=cmap(norm(deviation_from_initial[j])), linewidth=2)

ax1.set_xlabel('$t \\times f_{y}$', fontsize=15)
ax1.set_ylabel('$x^{\prime}(t) - x^{\prime}(0)$', fontsize=15)
ax1.set_title('$x^{\prime}(t) = x_{i}(t) -C_{x}(t)$ of discs id 108 to 117', fontsize=15)
ax1.tick_params(axis='both', which='both', direction='in', labelsize=15)
ax1.set_xscale('log')

# Create a colorbar for the first plot
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Only needed for ScalarMappable; no data needed
cbar = fig.colorbar(sm, ax=ax1, orientation='horizontal', pad=0.005, location='top', shrink=0.3, anchor=(0.0, 1.0))
cbar.ax.tick_params(labelsize=10)
cbar.set_label('$Deviation~from~Initial~Value$', fontsize=10)
ax1.grid(False)

# Plotting Vx vs T in the second subplot
ax2.plot(T_subset * Fy, Vx_subset / Fy, linewidth=1.0, linestyle='-', color='b', label='$V_{x}$')
ax2.set_xlabel('$t\\times f_{y}$', fontsize=15)
ax2.set_ylabel('$\\frac{V_{x}(t)}{f_{y}}$', fontsize=15)
ax2.tick_params(axis='both', which='both', direction='in', labelsize=15)
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlim(T_subset.min() * Fy, T_subset.max() * Fy)
ax2.set_ylim(3e0, Vx.max() / Fy)
ax2.grid(False)

# Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')

tight_layout()

FigName = f"../plots/X-all-grains-BlockInterface-Fy0.0001-Fx0.00006-allDiscs"
savefig(FigName + ".pdf", bbox_inches='tight', pad_inches=0)
plt.show()

