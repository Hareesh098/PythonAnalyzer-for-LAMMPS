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
FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[i])+"-Fx"+str(Fx[i])+"-New.dat"
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
 print(j)
 DirPath0 = "/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Push"
 DirPath = DirPath0+"/nAtom"+str(nAtom)+"/Fy"+str(Fy[j])+"/Fx"+str(Fx[j])+"/"
 FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[j])+"-Fx"+str(Fx[j])+"-New.dat"
 InputFile = DirPath+FileName
 data = genfromtxt(InputFile)
 t = data[:,0]
 Cx = data[:,1]
 Vx = gradient(Cx, t)
 #ax.plot(t*float(Fy[i]),Vx[i]/float(Fy[i]),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy[i]))
 ax.plot(t*float(Fy[j]),Vx/float(Fy[j]),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy[j]))
ax.axhline(y=Fy_by_Fx, xmin=min(t*float(Fy[0])), xmax=max(t*float(Fy[0])), color='black',linewidth="0.8",linestyle="--", label="y="+str(Fy_by_Fx))
ax.set_xlabel('$t\\times f_{y}$',fontsize=15)
ax.set_ylabel('$\\frac{V_{x}(t)}{f_{y}}$',fontsize=15)
ax.set_title('nAtom = '+ str(nAtom)+', $\\frac{f_{x}}{f_{y}}=$'+str(Fy_by_Fx),fontsize=15)
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
ax.set_xscale('log')
ax.set_yscale('log')
#ax.set_xlim(0.7,1e4)
#ax.set_ylim(3e-05,1e0)
ax.grid(False)
# Adjust legend and make sure each line is clear
leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, borderaxespad=0)
for line in leg.get_lines():
    line.set_linewidth(1.0)

#Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()
FigName = f"../plots/Vx-nAtom"+str(nAtom)+"-Z"+str(Z)+"Fx-by-Fy-"+str(Fy_by_Fx)
savefig(FigName+".pdf",bbox_inches='tight', pad_inches=0)
#show()



