import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal, getcontext
import re
import subprocess
import sys

#Set decimal precision
getcontext().prec = 10

#Defining the square function 
def Sqr(x):
 return x * x

# Use subprocess to run the touch command
def remove(filename):
 subprocess.run(['rm', filename])

# Check the correct number of arguments
if len(sys.argv) != 6:
    print("Error occurred")
    print("Usage: ./get-LAMMPS-Overlap-dy.py Initfile.dat Pairfile.dat skip_header max_rows frames")
    sys.exit()

# Read the arguments from the command line
Initfilename = sys.argv[1]
Pairfilename = sys.argv[2]
headeroffset0 = int(sys.argv[3])
rowoffset0 = int(sys.argv[4])
frames = int(sys.argv[5])

# Define the pattern to search for and the file to search in
pattern = "ITEM: NUMBER OF ENTRIES"
filename = sys.argv[2]
skip_header_pair = np.zeros(frames, dtype=int)
max_rows_pair = np.zeros(frames, dtype=int)
max_contacts = np.zeros(frames, dtype=int)
# Open the file and search for the pattern
n = 0

with open(filename, 'r') as file:
 lines = file.readlines()  # Read all lines of the file
 for i in range(len(lines)):
  if re.search(pattern, lines[i]):  # If pattern matches the current line
   next_line = lines[i + 1].strip()  # Get the next line and strip whitespaces
   if next_line.isdigit():  # Check if the next line is an integer
    #print(n, next_line)  # Print the integer
    max_contacts[n] = next_line
    n += 1
 
headeroffset0 = 9
max_rows_pair[0] = max_contacts[0]
skip_header_pair[0] = headeroffset0
for n in range(1,len(max_rows_pair)):
 skip_header_pair[n] = skip_header_pair[n-1]+max_rows_pair[n-1]+headeroffset0 
 max_rows_pair[n] = max_contacts[n]
 #print(n, skip_header_pair[n] , max_contacts[n])
 #print(n, max_contacts[n])


# Load the Init data
data = np.genfromtxt(Initfilename, skip_header=9)
atomID = data[:, 0].astype(int)
molID = data[:, 1].astype(int)
atomType = data[:, 2].astype(int)
radius = data[:, 3]
mass = data[:, 4]
x = data[:, 5]
y = data[:, 6]
vx = data[:, 7]
vy = data[:, 8]
fx = data[:, 9]
fy = data[:, 10]

#Count the number of atoms of type 4
num_atoms = np.sum(atomType == 4)

#Initialize arrays for atom data
LowerBlockID = np.zeros(num_atoms, dtype=int)
LowerBlockX = np.zeros(num_atoms)
LowerBlockY = np.zeros(num_atoms)
LowerBlockHarmonicF = np.zeros(num_atoms)
LowerBlockDeltaIJ = np.zeros(num_atoms)
n = 0

for i in range(len(atomType)):
 if atomType[i] == 4:
  LowerBlockID[n] = atomID[i]
  LowerBlockX[n] = x[i]
  LowerBlockY[n] = y[i]
  n += 1
#for i in range(num_atoms):
# print(i, LowerBlockID[i])

# Open a file for writing, append mode so you don't overwrite on every iteration
remove('../data/DeltaIJ.dat')
with open('../data/DeltaIJ.dat', 'a') as file:
 for n in range(0,frames):
  #Load the dumplocal pair data
  data = np.genfromtxt(Pairfilename, skip_header=skip_header_pair[n],max_rows=max_rows_pair[n])
  pairID = data[:,0].astype(int)
  patomID1 = data[:,1].astype(int)
  patomID2 = data[:,2].astype(int)
  HarmonicFx = data[:,3] 
  HarmonicFy = data[:,4]
  RelativeNormVelox = data[:,5] 
  RelativeNormVelox = data[:,6]
  HarmonicF = np.sqrt(Sqr(HarmonicFx) + Sqr(HarmonicFy))
  RadIJ = radius[patomID1] + radius[patomID2]
  #Reset LowerBlockHarmonicF for each frame
  LowerBlockHarmonicF = np.zeros(num_atoms)
  k = 1; k = int(k)
  for i in range(0,num_atoms):
   for j in range(0,max_rows_pair[n]):
    if(patomID1[j] == LowerBlockID[i] or patomID2[j] == LowerBlockID[i]):
     LowerBlockHarmonicF[i] += HarmonicF[j]
     LowerBlockDeltaIJ[i] = LowerBlockHarmonicF[i]*RadIJ[j]
     print(k, LowerBlockDeltaIJ[i])
     k += 1 
    #Add any further data processing or logic here...
  #plt.scatter(LowerBlockX,LowerBlockY, alpha=0.3,c=LowerBlockHarmonicF, s=30,cmap='rainbow')
  #plt.scatter(LowerBlockX,LowerBlockY, alpha=0.3,c=LowerBlockDeltaIJ, s=30,cmap='rainbow')
  #Here printing the total force on the lower discs of the block
  #for i in range(0,num_atoms):
  #print(LowerBlockHarmonicF[i])

  #Write the total force for each atom in the frame to the file with a space between them
  #file.write(" ".join(map(str, LowerBlockHarmonicF)))
  file.write(" ".join(map(str, LowerBlockDeltaIJ)))
  #Write a newline after each frame's data
  file.write("\n")

#plt.colorbar()  
plt.show()



