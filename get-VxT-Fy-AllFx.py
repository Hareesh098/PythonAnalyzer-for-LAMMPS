from pylab import *
from decimal import Decimal, getcontext
# Set the precision high enough
getcontext().prec = 10
from datetime import datetime
from scipy.signal import find_peaks

deltaT0 = 1e-3
nAtom =  130304
Z = 5.9894

# Check the correct number of arguments
if len(sys.argv) != 2:
    print("Error occurred")
    print("Usage: ./get-VxT-Fy-AllFx.py #FyValue")
    sys.exit()

nAtom = 130304
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
FxStart = Decimal(0.1)*FyEnd
FxEnd = Decimal(1.0)*FyEnd
deltaFx = Decimal(0.1)*FyEnd
#deltaFx = Decimal(1e-7)
FxNLoop = ((Decimal(FxEnd) - Decimal(FxStart))/Decimal(deltaFx)) + 1
FxNLoop = int(FxNLoop)

# Update Fx array values and print with proper formatting
# Initialize arrays
Fx = np.zeros(FxNLoop)
for i in range(FxNLoop):
 Fx[i] = float(FxStart + i * deltaFx)
 #print(Fx[i])

DirPath0 = f"/mt/fielding/hcharan/Work/Elastic-Network/Friction/Runs/Push/nAtom130304/"

for i in range(0,FyNLoop):
 output_data2 = []  # Initialize an empty list to accumulate data for all Fx values
 for j in range(0,FxNLoop): #FxNLoop
  DirPath = DirPath0+"Fy"+str(Fy[i])+"/Fx"+str(Fx[j])+"/"
  FileName = f"COM-nAtom"+str(nAtom)+"-Z"+str(Z)+"-Fy"+str(Fy[i])+"-Fx"+str(Fx[j])+".dat"
  InputFile = DirPath+FileName

  data = genfromtxt(InputFile)
  t = data[:,0]
  Cx = data[:,1]
  Vx = gradient(Cx, t)
  #plot(t,Vx,linewidth="0.5",linestyle="-",label='$f_{x}$ = '+str(Fx[j]))
  
  #Find indices of local minima
  min_indices, _ = find_peaks(-Vx)  # Invert y to treat minima as peaks
  
  #Find the first time Vx exceeds 0.0056
  condition = Vx > 100*Fy[i] #0.1
  indices = np.where(condition)[0]  # Find the indices where the condition is true
  
  #Save t, Vx to a separate data file
  output_data1 = column_stack((t, Vx))
  OutFileName1 = f"VeloX-nAtom{nAtom}-Z{Z}-Fy{Fy[i]}-Fx{Fx[j]}.dat"
  savetxt("../data/" + OutFileName1, output_data1, header="#t VeloX", comments='')
 
  #Append Fx, t_yield to the accumulated list (only if minima exist)
  #if len(min_indices) > 0:
  # t_yield = t[min_indices[0]] #Get the time corresponding to the first minima of Vx
  # output_data2.append([Fx[j], t_yield])
 
  if len(indices) > 0:
   t_yield = t[indices[0]]  #Get the time corresponding to the first time Vx > 0.1
   output_data2.append([Fx[j], t_yield])

  #Save all Fx, t_yield values for the current Fy to a separate data file
  if output_data2:
   output_data2_array = column_stack(output_data2)
   OutFileName2 = f"Fx-Tyield-nAtom{nAtom}-Z{Z}-Fy{Fy[i]}-VxbyFyCrossing.dat"
   #OutFileName2 = f"Fx-Tyield-nAtom{nAtom}-Z{Z}-Fy{Fy[i]}-Minima.dat"
   savetxt("../data/" + OutFileName2, output_data2_array.T, header="#Fx Tyield", comments='')
 print(f"Done with Fy = {Fy[i]}") 
show()  

