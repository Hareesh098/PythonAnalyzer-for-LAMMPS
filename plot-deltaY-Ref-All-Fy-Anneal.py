from pylab import *
from decimal import Decimal, getcontext
# Set the precision high enough
getcontext().prec = 10
from datetime import datetime
import matplotlib.ticker as mtick
# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

deltaT0 = 1e-3
nAtom =  130304
Z = 5.9894 

FyStart = 0.0001
FyEnd = 0.0019
deltaFy = 0.0001
FyNLoop = ((Decimal(FyEnd) - Decimal(FyStart))/Decimal(deltaFy)) + 1
FyNLoop =int(FyNLoop)
Fy = zeros(FyNLoop)
DeltaCy = zeros(FyNLoop)

#Plotting here
fig, ax = subplots(figsize=(6.4, 4.8)) 
for j in range(0,FyNLoop):
 Fy[j] = FyStart +  j * deltaFy
 Fy[j] = "{:.3g}".format(Fy[j])
 DirPath = "/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Reference/Annealing-Force"
 DirPath += "/nAtom"+str(nAtom)+"/Fy"+str(Fy[j])+"/"
 FileName = f"COM-nAtom{nAtom}-Z{Z}-Fy{Fy[j]}-Ref.dat"
 InputFile = DirPath+FileName
 data = genfromtxt(InputFile)
 t = data[:,0]
 Cy = data[:,2]
 DeltaCy[j] = Cy[0] - Cy[len(Cy)-1] 

# Perform least-squares linear fit (y = mt + c) on filtered data
coefficients = polyfit(Fy, DeltaCy, 1)  # Fit a 1st degree polynomial (linear fit)
linear_fit = poly1d(coefficients)
m = f"{coefficients[0]:.4f}"
c = f"{coefficients[1]:.4f}"
ax.plot(Fy,DeltaCy,"o", linewidth="1")
ax.plot(Fy, linear_fit(Fy), '--k', linewidth="1")
ax.set_xlabel('$f_{y}$',fontsize=15)
ax.set_ylabel('$\\Delta C_{y}$',fontsize=15)
ax.set_title(f"nAtom = {nAtom}, $f_{{y}}$ = all, $f_{{x}}$ = 0",fontsize=15)
ax.text(0.0007,2.5,f"Fit:$\\Delta C_{{y}} = {m} \\times f_{{y}} + {c}$",fontsize=15)
ax.tick_params(axis='both', which='major', labelsize=15)
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
ax.grid(False)

# Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()

FigName = f"../plots/DeltaCy-nAtom"+str(nAtom)+"-Z"+str(Z)+"-AllFy-Fx0-Reference-AnnealForce"
savefig(FigName+".pdf")
show()



