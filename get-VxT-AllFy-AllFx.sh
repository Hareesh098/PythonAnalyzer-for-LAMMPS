# Start value
Fystart=0.0001
# End value
Fyend=0.0019
# Step value
Fystep=0.0001

# Generate the array
value=$Fystart
while (( $(echo "$value <= $Fyend" | bc -l) )); do
 Fy+=("$(printf "%.4g" $value)")
 value=$(echo "$value + $Fystep" | bc)
done
FystepEnd=${#Fy[@]}

for ((i=0;i<$FystepEnd;i++)); do
 python get-VxT-Fy-AllFx.py ${Fy[$i]}
done
