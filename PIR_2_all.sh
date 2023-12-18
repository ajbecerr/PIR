#!/bin/sh

for i in {1..8}
do
  for j in {1..8}
  do 
    sbatch PIR_2_1.sh II 0 $i $j II
    sbatch PIR_2_1.sh HH 0 $i $j IZ
    sbatch PIR_2_1.sh HH 0 $i $j ZZ
  done
done

for i in {1..8}
do
  for j in {1..8}
  do 
    sbatch PIR_2_1.sh II $i 0 $j II
    sbatch PIR_2_1.sh HH $i 0 $j IZ
    sbatch PIR_2_1.sh HH $i 0 $j ZZ
  done
done
