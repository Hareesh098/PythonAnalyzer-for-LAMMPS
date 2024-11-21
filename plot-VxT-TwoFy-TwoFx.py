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
if(len(sys.argv) != 5):
 print("Error occurred")
 print("Usage: ./plot-VxT-TwoFy-TwoFx.py #Fy1 #Fx1 #Fy2 #Fx2")
 sys.exit()


nAtom = 130304
Z = 5.9894

# Generate the Fy array
Fy1 = str(sys.argv[1])
Fx1 = str(sys.argv[2])
Fy2 = str(sys.argv[3])
Fx2 = str(sys.argv[4])

DirPath0 = "/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Push"
DirPath = DirPath0+"/nAtom"+str(nAtom)+"/Fy"+str(Fy1)+"/Fx"+str(Fx1)+"/"
FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy1)+"-Fx"+str(Fx1)+"-New.dat"
InputFile = DirPath+FileName
data = genfromtxt(InputFile)
t1 = data[:,0]
Cx1 = data[:,1]
Vx1 = gradient(Cx1, t1)

DirPath = DirPath0+"/nAtom"+str(nAtom)+"/Fy"+str(Fy2)+"/Fx"+str(Fx2)+"/"
FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy2)+"-Fx"+str(Fx2)+"-New.dat"
InputFile = DirPath+FileName
data = genfromtxt(InputFile)
t2 = data[:,0]
Cx2 = data[:,1]
Vx2 = gradient(Cx2, t2)

#Plotting here
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
ax.plot(t1*float(Fy1),Vx1/float(Fy1),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy1))
ax.plot(t2*float(Fy2),Vx2/float(Fy2),linewidth="0.8",linestyle="--",label='$f_{y}$ = '+str(Fy2))
#ax.plot(t1,Vx1/float(Fy1),linewidth="0.8",linestyle="-",label='$f_{y}$ = '+str(Fy1))
#ax.plot(t2,Vx2/float(Fy2),linewidth="0.8",linestyle="--",label='$f_{y}$ = '+str(Fy2))
ax.set_xlabel('$t\\times f_{y}$',fontsize=15)
ax.set_ylabel('$\\frac{V_{x}(t)}{f_{y}}$',fontsize=15)
ax.set_title('nAtom = '+ str(nAtom)+', $\\frac{f_{x}}{f_{y}}=0.6$',fontsize=15)
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
ax.set_xscale('log')
ax.set_yscale('log')
leg = ax.legend(loc='upper left',fontsize=10)
for line in leg.get_lines():
 line.set_linewidth(1.0)
 ax.grid(False)

#Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()
FigName = f"../plots/Vx-nAtom"+str(nAtom)+"-Z"+str(Z)+"-TwoFy-TwoFx"
savefig(FigName+".pdf",bbox_inches='tight', pad_inches=0)
show()



