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
FileName = f"yMatrix.dat"
InputMatrixFile = DirPath+FileName
data = np.loadtxt(InputMatrixFile)
data = data.T # Transpose so that the time increases in column 
deltaT = 0.001
frames = 1014
MyEvery = 1e4
time = arange(1, frames+1)
time = time*deltaT*MyEvery
NgrainsStart = 0
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
Cy = COMdata[:, 2]

# Extract every 100th line, starting from index 0 (i.e., indices 0, 101, 201, ...)
T_subset = T[::100]
Cx_subset = Cx[::100]
Cy_subset = Cy[::100]

# Fy values
Fy = 0.0001
j = 0
fig, ax1 = plt.subplots(figsize=(6.4, 4.8))  # Create a figure with a single subplot
# Plotting x vs time in the first subplot with color coding based on initial value
for i in range(NgrainsStart, NgrainsEnd, NgrainsDelta):
 y = data[:, i]
 y = y - Cy_subset
 deviation_from_initial = y - y[0]
 # Define the colormap
 cmap = get_cmap('rainbow')  # rainbow=>best #brg=>2nd best #viridis=>3rd best
 norm = Normalize(vmin=-0.05, vmax=0.05) 

 # Plot each line segment with color coding based on the value of y
 for j in range(len(y) - 1):
  ax1.plot(time[j:j+2]*Fy, y[j:j+2], color=cmap(norm(deviation_from_initial[j])), linewidth=2)

# Set labels, title, and axis settings for ax1
ax1.set_xlabel('$t \\times f_{y}$', fontsize=15)
ax1.set_ylabel('$y^{\prime}(t) - y^{\prime}(0)$', fontsize=15, color='black')
ax1.set_title('$y^{\prime}(t) = y_{i}(t) -C_{y}(t)$ of all discs', fontsize=15)
# Set tick parameters for y-axis of ax1 and color to magenta
ax1.tick_params(axis='y', which='both', direction='in', labelsize=15, color='black')
# Set tick parameters for x-axis of ax1 and remove upper ticks
ax1.tick_params(axis='x', which='both', direction='in', top=False, labelsize=15)
ax1.set_xscale('log')
# Create a twin x-axis for ax1
ax1t = ax1.twiny()  # Create a twin of x-axis on top that shares the same data
ax1t.set_xscale('log')
ax1.set_xlim(1e-03, max(T_subset*Fy))
ax1t.set_xlim(ax1.get_xlim())  # Make sure the limits are shared
ax1t.xaxis.set_visible(False)  # Hide the twin x-axis completely

# Create a colorbar for the first plot
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  # Only needed for ScalarMappable; no data needed
cbar = fig.colorbar(sm, ax=ax1, orientation='horizontal', pad=0.005, location='top', shrink=0.3, anchor=(0.0, 1.0))
cbar.ax.tick_params(labelsize=10)
cbar.set_label('$Deviation~from~Initial~Value$', fontsize=10)
# Adjust the colorbar location
cbar.ax.set_position([0.15, 0.88, 0.7, 0.03])  # [left, bottom, width, height]
ax1.grid(False)

# Plotting Vx vs T in the second subplot
CxLabelColor = 'magenta'
ax2 = ax1.twinx()  # Create a twin y-axis for the same subplot
ax2.plot(T_subset * Fy, Cx_subset-Cx_subset[0], linewidth=2.0, linestyle='-', color=CxLabelColor, label='$C_{x}$')
ax2.set_ylabel('$C_{x}(t)$', fontsize=15, color=CxLabelColor)
# Set tick parameters for y-axis only and color to magenta for ax2
ax2.tick_params(axis='y', which='both', direction='in', labelsize=15, colors=CxLabelColor)
# Set tick parameters for x-axis to remove upper x-ticks for ax2
ax2.tick_params(axis='x', which='both', direction='in', top=False, bottom=False, labelsize=15)
# Explicitly turn off the visibility of upper x-ticks for ax2
ax2.xaxis.set_ticks_position('none')  # Ensure no ticks at the top
ax2.set_yscale('log')
#ax2.set_ylim(3e0, Vx.max() / Fy)
ax2.grid(False)

# Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')

tight_layout()
FigName = f"../plots/DyCxT-all-grains-BlockInterface-Fy0.0001-Fx0.00006-TwinXaxis-allDisc"
savefig(FigName + ".pdf", bbox_inches='tight', pad_inches=0)
plt.show()

