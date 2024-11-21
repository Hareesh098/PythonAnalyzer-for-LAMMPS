from pylab import *
import matplotlib.ticker as ticker
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
from scipy.signal import find_peaks

# Check the correct number of arguments
if len(sys.argv) != 2:
 print("Error occurred")
 print("Usage: .plot-VyT-AllFy-AllFx.py #FyValue")
 sys.exit()


nAtom = 180907 #130304
Z = 5.9894

# Generate the Fy array
FyStart = Decimal(sys.argv[1])
FyEnd = FyStart
deltaFy = FyStart
FyNLoop = ((Decimal(FyEnd) - Decimal(FyStart))/Decimal(deltaFy)) + 1
FyNLoop =int(FyNLoop)
# Initialize arrays
Fy = np.zeros(FyNLoop)
for i in range(0,FyNLoop):
 Fy[i] =  (i+1)*deltaFy
 Fy[i] = round(Fy[i], 4)  # Equivalent to "%.4g" formatting in shell

# Generate the Fx array
FxStart = Decimal(0.5)*FyEnd
FxEnd = Decimal(0.6)*FyEnd
#deltaFx = Decimal(0.1)*FyEnd
deltaFx = Decimal(1e-7)
FxNLoop = ((Decimal(FxEnd) - Decimal(FxStart))/Decimal(deltaFx)) + 1
FxNLoop = int(FxNLoop)

#Update Fx array values and print with proper formatting
#Initialize arrays
Fx = np.zeros(FxNLoop)
for i in range(FxNLoop):
 Fx[i] = float(FxStart + i * deltaFx)
 #print(Fx[i])


#Flags
colorbarFlag = 1

#Define the colormap
cmap = get_cmap('rainbow') #rainbow=>best #brg=>2nd best #viridis=>3rd best
norm = Normalize(FxStart, FxEnd) # Normalize Z_values to the range [0, 1] For Fx
DirPath0 = "/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Push"

#Plotting here
fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
for i in range(0,FyNLoop):
 for j in range(0,FxNLoop,1): #FxNLoop
  DirPath = DirPath0+"/nAtom"+str(nAtom)+"/Fy"+str(Fy[i])+"/Fx"+str(Fx[j])+"/"
  FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[i])+"-Fx"+str(Fx[j])+".dat"
  InputFile = DirPath+FileName
  data = genfromtxt(InputFile)
  t = data[:,0]
  Cx = data[:,1]
  Vx = gradient(Cx, t)
  if(colorbarFlag == 0):
   ax.plot(t*Fy,Vx/Fy,linewidth="0.8",linestyle="-",label='$f_{x}$ = '+str(Fx[j]))
  elif(colorbarFlag == 1):
   color = cmap(norm(float(Fx[j])))    
   ax.plot(t,Vx,linewidth="0.5",color=color,linestyle="-",label='$f_{x}$ = '+str(Fx[j]))
   #ax.plot(t*Fy,Vx/Fy,linewidth="0.5",color=color,linestyle="-",label='$f_{x}$ = '+str(Fx[j]))

#ax.set_xlabel('$t$',fontsize=15)
#ax.set_ylabel('$V_{x}(t) = \\frac{dC_{x}(t)}{dt}$',fontsize=15)
ax.set_xlabel('$t\\times f_{y}$',fontsize=15)
ax.set_ylabel('$\\frac{V_{x}(t)}{f_{y}}$',fontsize=15)
#ax.set_xlim(8e3,1e5)
#ax.set_ylim(3e-7,0.5)
#ax.text(2,2e-6,"$f_{x}^{\star}$ = 0.000244",fontsize=15)
ax.set_title('nAtom = '+ str(nAtom)+', $f_{y}$ = '+str(Fy[i]),fontsize=15)
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
 ax.grid(True)

# Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()
FigName = f"../plots/Vx-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[i])+"-AllFx"
savefig(FigName+".pdf",bbox_inches='tight', pad_inches=0)
show()



