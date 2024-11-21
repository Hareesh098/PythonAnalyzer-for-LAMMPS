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
FyEnd = 1e-04
deltaFy = 1e-04
FyNLoop = int(((Decimal(FyEnd) - Decimal(FyStart)) / Decimal(deltaFy)) + 1)

FxStar = [6e-05,0.00012,0.00015,0.0002,0.0002,0.00024,0.00028,0.00032,  
0.00027,0.0003,0.00033,0.00036,0.00039,0.00042,0.00045,0.00032,0.00034,   
0.00036,0.00038]

VinfStar = [ 3.220660650795252877e-01,3.844441132164320152e-01,
3.478535906172055547e-01,3.547141367628228181e-01,
2.820106493693401717e-01,2.806288839542503410e-01,
2.789838796045387426e-01,2.773593026979597198e-01,
1.973954228180900827e-01,1.965216069559119205e-01,
1.957641951134974079e-01,1.951310860461035190e-01,
1.946667142276510276e-01,1.942184484685185453e-01,
1.939579820948438282e-01,1.109581449743473058e-01,	
1.107514708767212142e-01,1.109944988941151678e-01,
1.106050463749852497e-01]
FxStarFlag = 1
alpha = 0.65

markers = ['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', 'X', 'd', '|', '_', '1', '2']

# Create the figure and axis outside the loop to plot everything together
fig, ax = subplots(figsize=(6.4, 4.8))
# Loop over all Fy values
for i in range(0,2):
    Fy = FyStart + i * deltaFy  # Update Fy value for each iteration
    
    # Load data file corresponding to current Fy
    FileName = f"../data/Fx-Vinf-nAtom130304-Z5.9894-Fy{Fy:.4g}.dat"
    data = genfromtxt(FileName)
    Fx = data[:, 0]
    Vinf = data[:, 1]

    # Perform least-squares linear fit (y = mt + c) on filtered data
    mask = Vinf > 5e-05
    Vinf_filtered = Vinf[mask]
    Fx_filtered = Fx[mask]
    coefficients = polyfit(Fx_filtered, Vinf_filtered, 1)
    linear_fit = poly1d(coefficients)
    m = f"{coefficients[0]:.6e}"
    c = f"{coefficients[1]:.4f}"

    # Generate Fx array for fitting
    FxFit = linspace(0, max(Fx), 1000)

    # Plot the current Fy data and fit
    if(FxStarFlag == 0):
     ax.plot(Fx, Vinf, "o", markersize=5, label=f"Sim Fy={Fy:.4g}")
     ax.plot(FxFit, linear_fit(FxFit), '--', linewidth=1, label=f"Fit Fy={Fy:.4g}, $m$={m}, $c$={c}")
    # Plot the current Fy data and fit
    elif(FxStarFlag == 1):
     #ax.plot(Fx/FxStar[i], Vinf/VinfStar[i], "o", markersize=5, label=f"$f_{{y}}$={Fy:.4g}")
     #ax.plot(Fx, Vinf, "o", markersize=5, marker=markers[i], alpha=float(alpha),label=f"$f_{{y}}$={Fy:.4g}")
     ax.plot(Fx/Fy, Vinf/Fy, "o", markersize=3, marker=markers[i], alpha=float(alpha),label="$f_{y}$="+str(Fy))

         
# Set labels and title
if(FxStarFlag == 0):
 ax.set_xlabel('$f_{x}$', fontsize=15)
 ax.set_ylabel('$v_{\\infty}$', fontsize=15)
if(FxStarFlag == 1):
 #ax.set_xlabel('$\\frac{f_{x}}{f_{x}^{\star}}$', fontsize=20)
 #ax.set_ylabel('$\\frac{v_{\\infty}}{v_{\\infty}{\star}}$', fontsize=20) 
 #ax.set_xlabel('$\\frac{f_{x}}{f_{y}}$', fontsize=15)
 #ax.set_ylabel('$v_{\\infty}$', fontsize=15)
 ax.set_xlabel('$\\frac{f_{x}}{f_{y}}$', fontsize=15) 
 ax.set_ylabel('$\\frac{v_{\\infty}}{f_{y}}$', fontsize=15)
 ax.text(0.2,3000,'Collapsing only\nfor higher $f_{y}$ values', fontsize=15)
 
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
 FigName = f"../plots/Fx-Vinf-nAtom130304-Z5.9894-Multiple-Fy"
elif(FxStarFlag == 1):
 #FigName = f"../plots/Fx_by_FxStar-Vinf_by_VinfStar-nAtom130304-Z5.9894-Multiple-Fy"
 FigName = f"../plots/FxTilde-VinfFxTilde-nAtom130304-Z5.9894-Multiple-Fy"
 #FigName = f"../plots/Fx_by_Fy-Vinf-nAtom130304-Z5.9894-Multiple-Fy"
savefig(FigName + ".pdf",bbox_inches='tight',pad_inches=0)
show()

