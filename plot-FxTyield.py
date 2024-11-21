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

# Check the correct number of arguments
if(len(sys.argv) != 3):
 print("Error occurred")
 print("Usage: ./plot-FxTyield.py #FyStart #FyEnd")
 sys.exit()

# Parameters
nAtom = 130304
Z = 5.9894
# Generate the Fy array
FyStart = Decimal(sys.argv[1])
FyEnd = Decimal(sys.argv[2])
deltaFy = 0.0001
FyNLoop = ((Decimal(FyEnd) - Decimal(FyStart))/Decimal(deltaFy)) + 1
FyNLoop =int(FyNLoop)
# Initialize arrays
Fy = np.zeros(FyNLoop)
for i in range(0,FyNLoop):
 Fy[i] =  (i+1)*deltaFy
 Fy[i] = round(Fy[i], 4)  # Equivalent to "%.4g" formatting in shell

# Prepare figure
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
j=0
filename = "../data/Fx-Tyield-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[j])+"-VxbyFyCrossing.dat"
data = genfromtxt(filename)
Fx = data[:, 0]
t_yield = data[:, 1]
ax.plot(Fx/float(Fy[j]), log(t_yield * float(Fy[j])), '-o', linewidth=0.8,label='$f_{{y}}$ ='+str(Fy[j]))
# Loop through Fy values and read corresponding data
k=1
for i in range(1,FyNLoop):
 k = k*2; j = k-1
 if j > FyNLoop:
  break
 #Construct filename
 #filename = f"../data/Fx-Tyield-nAtom{nAtom}-Z{Z}-Fy{Fy[{i}]:.4g}-VxbyFyCrossing.dat"
 filename = "../data/Fx-Tyield-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[j])+"-VxbyFyCrossing.dat"
 #Check if the file exists
 if os.path.exists(filename):
  data = genfromtxt(filename)
  Fx = data[:, 0]
  t_yield = data[:, 1]
        
  # Plot data
  ax.plot(Fx/float(Fy[j]), log(t_yield * float(Fy[j])), '-o', linewidth=0.8,label='$f_{{y}}$ ='+str(Fy[j]))
 else:
  print(f"Warning: File '{filename}' not found.")

# Set labels, title, and legend
ax.set_xlabel('$\\frac{f_{x}}{f_{y}}$', fontsize=15)
ax.set_ylabel('log($t_{yield} \\times f_{y})$', fontsize=15)
#ax.set_title(f'nAtom = {nAtom}, $for~local~minima~of~V_{{x}}(t)$', fontsize=15)
ax.set_title("nAtom ="+str(nAtom) + ";~~$Criterion~~\\frac{V_{x}(t)}{f_{y}} > 10^2$", fontsize=15)
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
FigName = f"../plots/Fx-Tyield-nAtom{nAtom}-Z{Z}-MultipleFy-VxbyFyCrossing"
savefig(FigName + ".pdf", bbox_inches='tight', pad_inches=0)

# Show plot
show()

