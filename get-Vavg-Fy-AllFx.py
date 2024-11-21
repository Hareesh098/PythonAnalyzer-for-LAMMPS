import os
import sys
import numpy as np
from decimal import Decimal, getcontext

# Set the precision high enough
getcontext().prec = 10

nAtom = 130304
Z = 5.9894

# Check the correct number of arguments
if len(sys.argv) != 2:
 print("Error occurred")
 print("Usage: ./get-Vinf-Fy-AllFx.py #FyValue")
 sys.exit()

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
FxStart = Decimal(0.1)*FyEnd
FxEnd = FyEnd
deltaFx = Decimal(0.1)*FyEnd
FxNLoop = ((Decimal(FxEnd) - Decimal(FxStart))/Decimal(deltaFx)) + 1
FxNLoop =int(FxNLoop)
# Initialize arrays
Fx = np.zeros(FxNLoop)
for i in range(0,FxNLoop):
 Fx[i] =  (i+1)*deltaFx
 Fx[i] = round(Fx[i], 5)  # Equivalent to "%.5g" formatting in shell

# Create an array to store results
results = []

for i in range(0,FyNLoop):
 output_file = f"../data/Fx-Vavg-nAtom{nAtom}-Z{Z}-Fy{Fy[i]:.4g}.dat"
    
 # Remove the output file if it exists
 if os.path.exists(output_file):
  os.remove(output_file)
    
 for k in range(0,FxNLoop):
  data_file = f"../data/VeloX-nAtom{nAtom}-Z{Z}-Fy{Fy[i]:.4g}-Fx{Fx[k]:.5g}.dat"
  data = np.loadtxt(data_file)
  Vx = data[:,1]     
  avg_value = np.mean(Vx)      
  # Append the Fx and last_value to the output file
  with open(output_file, 'a') as f_out:
   f_out.write(f"{Fx[k]:.4g} {avg_value}\n")
    
 print(f"Done with Fy = {Fy[i]:.5g}")

