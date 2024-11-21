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
if len(sys.argv) != 2:
 print("Error occurred")
 print("Usage: .plot-VyT-AllFy-AllFx.py #FyValue")
 sys.exit()

nAtom =  [57380, 130304, 131858, 207092, 203438, 300000, 400000, 500000]
nAtomID = 1
nAtomNLoop = 2

Z = [5.9938, 5.9894, 5.9894, 5.9938, 5.9938, 5.9908, 5.9925, 5.9934, 5.9942]
line_styles = ['-', '--', '-.', ':', '-']

# Generate the Fy array
FyStart = Decimal(sys.argv[1])
FyEnd = FyStart
deltaFy = FyStart
FyNLoop = ((Decimal(FyEnd) - Decimal(FyStart))/Decimal(deltaFy)) + 1
FyNLoop =int(FyNLoop)

# Generate the Fx array
FxStart = Decimal(0.1)*FyEnd
FxEnd = FyEnd
deltaFx = Decimal(0.1)*FyEnd
FxNLoop = ((Decimal(FxEnd) - Decimal(FxStart))/Decimal(deltaFx)) + 1
FxNLoop =int(FxNLoop)

#Flags
colorbarFlag = 1

#Define the colormap
cmap = get_cmap('rainbow') #rainbow=>best #brg=>2nd best #viridis=>3rd best
norm = Normalize(FxStart, FxEnd) # Normalize Z_values to the range [0, 1] For Fx
DirPath0 = "/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Push/"

#Plotting here
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
for i in range(nAtomID,nAtomNLoop):
 for j in range(0,FyNLoop):
  Fy = FyStart +  j * deltaFy
  Fy = "{:.3g}".format(Fy)
  for k in range(0,FxNLoop): #FxNLoop
   Fx = FxStart +  k * deltaFx
   Fx = "{:.4g}".format(Fx)
          
   DirPath = DirPath0+"/nAtom"+str(nAtom[i])+"/Fy"+str(Fy)+"/Fx"+str(Fx)+"/"
   FileName = f"COM-nAtom"+str(nAtom[i])+"-Z"+str(Z[i])+"-Fy"+str(Fy)+"-Fx"+str(Fx)+".dat"
   InputFile = DirPath+FileName

   data = genfromtxt(InputFile)
   t = data[:,0]
   Cy = data[:,2]
   Vy = gradient(Cy, t)
   if(colorbarFlag == 0):
    ax.plot(t,Vx,linewidth="0.8",linestyle="-",label='$f_{x}$ = '+str(Fx))
   elif(colorbarFlag == 1):
    color = cmap(norm(float(Fx)))    
    ax.plot(t,Vy,linewidth="0.5",color=color,linestyle="-",label='$f_{x}$ = '+str(Fx))

ax.set_xlabel('$t$',fontsize=15)
ax.set_ylabel('$V_{y}(t) = \\frac{dC_{x}(t)}{dt}$',fontsize=15)
#ax.set_xlim(8e3,1e5)
#ax.set_ylim(3e-7,0.5)
#ax.text(2,2e-6,"$f_{x}^{\star}$ = 0.000244",fontsize=15)
ax.set_title('nAtom = '+ str(nAtom[nAtomID])+', $f_{y}$ = '+str(Fy),fontsize=15)
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
ax.set_xscale('log')
ax.set_yscale('log')
if(colorbarFlag == 0):
 leg = ax.legend(loc='upper left',fontsize=10)
 for line in leg.get_lines():
  line.set_linewidth(1.0)

# Create a colorbar
if(colorbarFlag == 1):
 sm = cm.ScalarMappable(cmap=cmap, norm=norm)
 sm.set_array([])  # Only needed for ScalarMappable; no data needed
 cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.0)
 cbar.ax.tick_params(labelsize=10)
 cbar.set_label('$f_{x}$',fontsize=15)
 ax.grid(False)

# Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()
FigName = f"../plots/Vy-nAtom"+str(nAtom[nAtomID])+"-Z"+str(Z[nAtomID])+"-Fy"+str(Fy)+"-AllFx"
savefig(FigName+".pdf",bbox_inches='tight', pad_inches=0)
show()



