from pylab import *
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

# Set range of Fy values
FyStart = 1e-04
FyEnd = 19e-04
deltaFy = 1e-04
FyNLoop = int(((Decimal(FyEnd) - Decimal(FyStart)) / Decimal(deltaFy)) + 1)

FxStar = [6e-05,0.00012,0.00015, 0.0002, 0.0002, 0.0004]
VinfStar = [3.220660650795252877e-01,3.844441132164320152e-01,
3.478535906172055547e-01,3.547141367628228181e-01,
2.820106493693401717e-01]
FxStarFlag = 1
alpha = 0.3
# Create the figure and axis outside the loop to plot everything together
fig, ax = subplots(figsize=(6.4, 4.8))
# Loop over all Fy values
for i in range(0,5):
    Fy = FyStart + i * deltaFy  # Update Fy value for each iteration
    
    # Load data file corresponding to current Fy
    FileName = f"../data/Fx-Vavg-nAtom130304-Z5.9894-Fy{Fy:.4g}.dat"
    data = genfromtxt(FileName)
    Fx = data[:, 0]
    Vavg = data[:, 1]

    # Perform least-squares linear fit (y = mt + c) on filtered data
    mask = Vavg > 5e-05
    Vavg_filtered = Vavg[mask]
    Fx_filtered = Fx[mask]
    coefficients = polyfit(Fx_filtered, Vavg_filtered, 1)
    linear_fit = poly1d(coefficients)
    m = f"{coefficients[0]:.6e}"
    c = f"{coefficients[1]:.4f}"

    # Generate Fx array for fitting
    FxFit = linspace(0, max(Fx), 1000)

    # Plot the current Fy data and fit
    if(FxStarFlag == 0):
     ax.plot(Fx, Vavg, "o", markersize=5, label=f"Sim Fy={Fy:.4g}")
     ax.plot(FxFit, linear_fit(FxFit), '--', linewidth=1, label=f"Fit Fy={Fy:.4g}, $m$={m}, $c$={c}")
    # Plot the current Fy data and fit
    elif(FxStarFlag == 1):
     #ax.plot(Fx/FxStar[i], Vavg/VinfStar[i], "o", markersize=5, label=f"Sim Fy={Fy:.4f}")
     ax.plot(Fx/Fy, Vavg, "o", markersize=10, alpha=float(alpha),label=f"Sim Fy={Fy:.4g}")

         
# Set labels and title
if(FxStarFlag == 0):
 ax.set_xlabel('$f_{x}$', fontsize=15)
 ax.set_ylabel('$v_{\\infty}$', fontsize=15)
if(FxStarFlag == 1):
 #ax.set_xlabel('$\\frac{f_{x}}{f_{x}^{\star}}$', fontsize=15)
 #ax.set_ylabel('$\\frac{v_{\\infty}}{v_{\\infty}{\star}}$', fontsize=15) 
 ax.set_xlabel('$\\frac{f_{x}}{f_{y}}$', fontsize=15)
 ax.set_ylabel('$v_{\\infty}$', fontsize=15)
 
ax.grid(True)
ax.set_title(f'nAtom = 130304, Multiple $f_{{y}}$ Values', fontsize=15)
ax.tick_params(axis='both', which='major', labelsize=15)

# Adjust legend and make sure each line is clear
leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(1.0)

# Add timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()

# Save figure
if(FxStarFlag == 0):
 FigName = f"../plots/Fx-Vavg-nAtom130304-Z5.9894-Multiple-Fy"
elif(FxStarFlag == 1):
 #FigName = f"../plots/Fx_by_FxStar-Vavg-nAtom130304-Z5.9894-Multiple-Fy"
 FigName = f"../plots/Fx_by_Fy-Vavg-nAtom130304-Z5.9894-Multiple-Fy"
savefig(FigName + ".pdf")
show()

