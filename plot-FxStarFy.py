from pylab import *
from decimal import Decimal, getcontext
import matplotlib
import matplotlib.ticker as mtick
from matplotlib.colors import LogNorm, Normalize
from datetime import datetime
import os

# Set the precision high enough
getcontext().prec = 10

# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

# Parameters
nAtom = 130304
Z = 5.9894
# Set range of Fy values
FyStart = 1e-04
FyEnd = 19e-04
deltaFy = 1e-04
FyNLoop = int(((Decimal(FyEnd) - Decimal(FyStart)) / Decimal(deltaFy)) + 1)

markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', 'X', 'd', '|', '_', '1', '2']

#Prepare figure
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
for i in range(0,FyNLoop):
 Fy = FyStart + i * deltaFy  # Update Fy value for each iteration
 #Construct filename
 filename = f"../data/Fx-Tyield-nAtom{nAtom}-Z{Z}-Fy{Fy:.4g}-VxCrossing.dat"
    
 #Check if the file exists
 if os.path.exists(filename):
  data = genfromtxt(filename)
  Fx = data[:, 0]
  t_yield = data[:, 1]
  ax.plot(float(Fy),Fx[0]/float(Fy),markersize=10, marker=markers[i],label=f'$f_{{y}}$ = {Fy:.4g}')
 else:
  print(f"Warning: File '{filename}' not found.")

# Set labels, title, and legend
ax.set_xlabel('$f_{y}$', fontsize=15)
ax.set_ylabel('$\\frac{f^{\star}_{x}}{f_{y}}$', fontsize=15)
#ax.set_title(f'nAtom = {nAtom}, $for~local~minima~of~V_{{x}}(t)$', fontsize=15)
ax.set_title(f'nAtom = {nAtom}, $f_{{y}}~~vs.~~f^{{\star}}$', fontsize=15)
ax.tick_params(axis='both', which='both', direction='in', labelsize=15)

# Legend and grid
# Adjust legend and make sure each line is clear
leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(1.0)
ax.grid(False)

# Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')

# Adjust layout and save figure
tight_layout()
FigName = f"../plots/FxStar-by-Fy-vs-Fy-nAtom{nAtom}-Z{Z}"
savefig(FigName + ".pdf", bbox_inches='tight', pad_inches=0)

# Show plot
show()

