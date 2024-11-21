from pylab import *
from datetime import datetime
import matplotlib.ticker as mtick

# Ensure LaTeX is properly set up
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

    
DirPath = f"../data/"
FileName = f"yMatrix.dat"
InputMatrixFile = DirPath+FileName
data = np.loadtxt(InputMatrixFile)
data = data.T #Transpose so that the time increases in column 
deltaT = 0.001
frames = 1014
MyEvery=1e5
time = arange(1, frames+1)
time = time*deltaT*MyEvery
NgrainsStart = 0
NgrainsEnd = 10
NgrainsDelta = 1
atomID = arange(NgrainsStart, NgrainsEnd,1)

#Loading the COMx coordinates so that we get the block's discs' coordinates in
#the block frame of reference
COMdata = np.loadtxt("../data/COM-nAtom130304-Z5.9894-Fy0.0001-Fx6e-05.dat")
COMy = COMdata[:,2]
# Extract every 100th line, starting from index 0 (i.e., indices 0, 101, 201, ...)
COMy_subset = COMy[::100]

#Define the colormap
cmap = get_cmap('rainbow') #rainbow=>best #brg=>2nd best #viridis=>3rd best
norm = Normalize(NgrainsStart, NgrainsEnd) 
#color = cmap(norm(float(atomID))) 

fig, ax = subplots(figsize=(6.4, 4.8))  # Create a figure and axes
for i in range(NgrainsStart,NgrainsEnd,NgrainsDelta):
 y = data[:,i]
 #y = y - y[0]*0
 y = y - COMy_subset
 color = cmap(norm(i)) 
 ax.plot(time,y,linewidth="1",color=color)
ax.set_xlabel('$t$',fontsize=15)
ax.set_ylabel('$y$',fontsize=15)
ax.set_title('y(t) of all grains',fontsize=15)
ax.tick_params(axis='both', which='major', labelsize=15)
#ax.set_xscale('log')
#ax.set_yscale('log')

#Create a colorbar
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])  
cbar = fig.colorbar(sm, ax=ax, orientation='vertical', pad=0.0)
cbar.set_label('grain ids')
ax.grid(False)

#Add timestamp text
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
fig.text(0.99, 0.01, f"[Date and Time: {timestamp}]", transform=fig.transFigure, fontsize=8, horizontalalignment='right')
tight_layout()

FigName = f"../plots/Y-all-grains-BlockInterface"
savefig(FigName+".pdf")
show()



