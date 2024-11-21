# Start value
FyStart=0.0001
# End value
FyEnd=0.0019
for ((i=8;i<=8;i++)); do
 Fx_by_Fy=$(echo "$i * 0.1" | bc)
 python plot-VxT-Fx-by-Fy.py $FyStart $FyEnd $Fx_by_Fy
done
