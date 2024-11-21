#!/mt/data-fielding/hcharan/Installed-Softwares/anaconda3/bin/python
from numpy import *
from decimal import Decimal, getcontext
getcontext().prec = 10
import sys

# Check the correct number of arguments
if(len(sys.argv) != 5):
 print("Error occurred")
 print("Usage: ./plot-LAMMPS-Gen-Traj.py filename.dat skip_header max_rows frames")
 sys.exit()

# Read the arguments from command line
filename = sys.argv[1]
headeroffset0 = int(sys.argv[2])
rowoffset0 = int(sys.argv[3])
frames = int(sys.argv[4])
fxMatrix = []  #List to store x values for each frame

#Loop over multiple frames
for i in range(1, frames+1):  #frames loop
 headerSkip = i * headeroffset0 + (i - 1) * rowoffset0
    
 # Load the data
 data = genfromtxt(filename, skip_header=headerSkip, max_rows=rowoffset0)
    
 if(data.size == 0):
  print(f"Warning: No data read for frame {i}. Skipping.")
  continue
   
 #Extract data columns
 #data format = id radius x y vx vy fx fy
 atomID = data[:, 0]
 atomRadius = data[:, 1] 
 x = data[:, 2]  
 y = data[:, 3] 
 vx = data[:, 4]
 vy = data[:, 5]
 fx = data[:, 6]
 fy = data[:, 7]

    
 #Append x values to matrix
 fxMatrix.append(fx)

fxMatrix = array(fxMatrix).T
savetxt("../data/fxMatrix.dat", fxMatrix, delimiter=" ")


