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
 Fy[i] = "{:.4g}".format(Fy[i]) # Equivalent to "%.4g" formatting in shell

# Generate the Fx array
FxStart = Decimal(0.1)*FyEnd
FxEnd = Decimal(1.0)*FyEnd
deltaFx = Decimal(0.1)*FyEnd
#deltaFx = Decimal(1e-7)
FxNLoop = ((Decimal(FxEnd) - Decimal(FxStart))/Decimal(deltaFx)) + 1
FxNLoop =int(FxNLoop)

# Update Fx array values and print with proper formatting
# Initialize arrays
Fx = np.zeros(FxNLoop)
for i in range(FxNLoop):
 Fx[i] = float(FxStart + i * deltaFx)

# Create an array to store results
results = []

for i in range(0,FyNLoop):
 output_file = f"../data/Fx-Vinf-nAtom{nAtom}-Z{Z}-Fy{Fy[i]:.4g}.dat"
    
 # Remove the output file if it exists
 if os.path.exists(output_file):
  os.remove(output_file)
    
 for k in range(0,FxNLoop):
  data_file = f"../data/VeloX-nAtom{nAtom}-Z{Z}-Fy{Fy[i]:.4g}-Fx{Fx[k]:.7g}.dat"
        
  # Get the last non-empty item from the second column of the data file
  try:
   last_value = None
   with open(data_file, 'r') as f:
    for line in f:
     if line.strip():  # Ensure it's a non-empty line
      last_value = line.split()[1]  # Get the second column
      if last_value == 'nan':
       last_value = 0.0  # Handle NaN case
  except FileNotFoundError:
   last_value = "0"  # Handle missing file case or assign a default value
        
  # Append the Fx and last_value to the output file
  with open(output_file, 'a') as f_out:
   f_out.write(f"{Fx[k]:.7g} {last_value}\n")
    
 print(f"Done with Fy = {Fy[i]:.4g}")

