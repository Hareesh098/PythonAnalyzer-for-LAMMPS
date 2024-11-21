import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from decimal import Decimal, getcontext
# Set the precision high enough
getcontext().prec = 10
from datetime import datetime
import matplotlib.ticker as mtick
from matplotlib.colors import LogNorm, Normalize
# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

from pylab import *
from decimal import Decimal, getcontext
# Set the precision high enough
getcontext().prec = 10
from datetime import datetime
import matplotlib.ticker as mtick
from matplotlib.colors import LogNorm, Normalize
# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

# Check the correct number of arguments
if(len(sys.argv) != 4):
 print("Error occurred")
 print("Usage: ./plot-VxT-Fy-AllFx.py #FyStart #FyEnd Fy_by_Fx")
 sys.exit()

nAtom = 130304
Z = 5.9894

# Generate the Fy array
FyStart = Decimal(sys.argv[1])
FyEnd = Decimal(sys.argv[2])
deltaFy = FyStart
FyNLoop = ((Decimal(FyEnd) - Decimal(FyStart))/Decimal(deltaFy)) + 1
FyNLoop =int(FyNLoop)
# Initialize arrays
Fy = np.zeros(FyNLoop)
for i in range(0,FyNLoop):
 Fy[i] =  (i+1)*deltaFy
 Fy[i] = round(Fy[i], 4)  # Equivalent to "%.4g" formatting in shell

Fy_by_Fx = float(sys.argv[3])

# Update Fx array values and print with proper formatting
# Initialize arrays
Fx = np.zeros(FyNLoop)
for i in range(FyNLoop):
 Fx[i] = float(Fy_by_Fx * Fy[i])
 Fx[i] = round(Fx[i], 7)
 #print(Fx[i])

#Plotting here
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
i=0
DirPath0 = "/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Push"
DirPath = DirPath0+"/nAtom"+str(nAtom)+"/Fy"+str(Fy[i])+"/Fx"+str(Fx[i])+"/"
FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[i])+"-Fx"+str(Fx[i])+".dat"
InputFile = DirPath+FileName
data = genfromtxt(InputFile)
t = data[:,0]
Cx = data[:,1]
Vx = gradient(Cx, t)
#ax.plot(t*float(Fy[i]),Vx[i]/float(Fy[i]),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy[i]))
ax.plot(t*float(Fy[i]),Vx/float(Fy[i]),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy[i]))
k=1
for i in range(1,FyNLoop):
 k = k*2; j = k-1
 if j > FyNLoop:
  break
 #print(j)
 DirPath0 = "/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Push"
 DirPath = DirPath0+"/nAtom"+str(nAtom)+"/Fy"+str(Fy[j])+"/Fx"+str(Fx[j])+"/"
 FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[j])+"-Fx"+str(Fx[j])+".dat"
 InputFile = DirPath+FileName
 data = genfromtxt(InputFile)
 t = data[:,0]
 Cx = data[:,1]
 Vx = gradient(Cx, t)
 #ax.plot(t*float(Fy[i]),Vx[i]/float(Fy[i]),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy[i]))
 ax.plot(t*float(Fy[j]),Vx/float(Fy[j]),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy[j]))
# Adjust legend and make sure each line is clear
leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(1.0)


# Parameters for simulation
fy_values = [0.0001, 0.0002, 0.0004, 0.0008, 0.0016]  # Different fy values
fx_over_fy = 0.6  # Fixed ratio fx/fy
time_extended = np.linspace(1, 10000, 500)  # Extended time range

# Function to simulate Vx over time for the numerical solution
def simulate_vx(fy, fx_over_fy, time):
    fx = fy * fx_over_fy
    damping_factor = fy * 1.3  # approximate damping scaling with fy
    initial_acceleration = fx
    M = 1 # assume block mass
    Vx = (initial_acceleration / damping_factor) * (1 - np.exp((-damping_factor * time)/M))
    return Vx

# Linear function for contact density scaling with fy
def contact_density_linear(fy):
    return 0.01 + (fy - 0.0001) * (0.16 - 0.01) / (0.0016 - 0.0001)

# Refined analytical function with nonlinear scaling of contact density
def refined_analytical_vx(fy, time):
    fx = fy * fx_over_fy
    zeta_b = 1  # body damping constant
    zeta_v = 1  # interface damping constant
    M = 100  # assume block mass
    contact_density_effect = contact_density_linear(fy) ** 1.5  # nonlinear scaling
    zeta_total = zeta_b + zeta_v * contact_density_effect
    Vx_analytical = (fx / zeta_total) * (1 - np.exp(-zeta_total * time / M))
    return Vx_analytical

# Plotting both analytical (refined) and numerical results on scaled axes
for fy in fy_values:
    scaled_time = time_extended * fy
    Vx_numerical = simulate_vx(fy, fx_over_fy, time_extended) / fy
    Vx_analytical = refined_analytical_vx(fy, time_extended) / fy

    # Plot numerical and refined analytical solutions
    ax.plot(scaled_time, Vx_numerical, linewidth="0.8",linestyle="--",label=f'$Theory f_y = {fy}$')
    #ax.plot(scaled_time, Vx_analytical, label=f'Refined Analytical $f_y = {fy}$', linestyle='--', alpha=0.7)

ax.set_xlabel('$t \\cdot f_y$',fontsize=15)
ax.set_ylabel('$V_x / f_y$',fontsize=15)
ax.set_title('Analytical Results',fontsize=15)
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
ax.set_xscale('log')
ax.set_yscale('log')

# Adjust legend and make sure each line is clear
leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(1.0)

#Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()


tight_layout()
plt.savefig("../plots/VxT-Analytical-Simulaitons.pdf",bbox_inches='tight', pad_inches=0)
plt.show()

