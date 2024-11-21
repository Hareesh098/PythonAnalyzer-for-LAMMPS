from numpy import arange, meshgrid, load
import numpy as np
from scipy.interpolate import griddata  # You need griddata from scipy
from decimal import Decimal, getcontext
# Set the precision high enough
getcontext().prec = 10
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Ensure LaTeX is properly set up
import matplotlib
matplotlib.rc('text', usetex=True)
matplotlib.rc('font', family='serif')
matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath}"

LowerBlockHarmonicF = np.loadtxt("../data/DeltaIJ.dat")
LowerBlockHarmonicF = LowerBlockHarmonicF.T
print(np.shape(LowerBlockHarmonicF))
deltaT = 0.001
frames = 102
MyEvery = 1e5
time = arange(0, frames)
time = time*deltaT*MyEvery
ids = np.arange(0,117)
X, Y = np.meshgrid(time, ids)

# Plot the matrix using contourf
fig = plt.figure(1)
ax = fig.add_subplot(111)
ax.grid(True)
#ax.set_aspect('auto')

plt.imshow(LowerBlockHarmonicF, origin='upper',cmap='rainbow')
#plt.contourf(X, Y, LowerBlockHarmonicF, origin='upper', interpolation='bilinear',cmap='rainbow')
plt.colorbar(label="Pair Force magnitude LowerBlockHarmonicF")
ax.tick_params(axis='both', which='both', direction='in',labelsize=15)
plt.xlabel("Time (s)",fontsize=15)
plt.ylabel("id",fontsize=15)
plt.title("LowerBlockHarmonicDeltaIJ")
plt.savefig("LowerBlockHarmonicDeltaIJ-nAtom130304-Z5.9894-Fy1e-4-Fx6e-5.pdf")
#plt.title("LowerBlockHarmonicForce")
#plt.savefig("LowerBlockHarmonicForce-nAtom130304-Z5.9894-Fy1e-4-Fx6e-5.pdf")
plt.show()

