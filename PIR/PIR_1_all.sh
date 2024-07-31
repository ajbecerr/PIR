#!/bin/sh

for i in {1..8}
do
  for j in {1..8}
  do 
    sbatch PIR_1_1.sh II 0 $i $j
    sbatch PIR_1_1.sh HH 0 $i $j
  done
done

for i in {1..8}
do
  for j in {1..8}
  do 
    sbatch PIR_1_1.sh II $i 0 $j
    sbatch PIR_1_1.sh HH $i 0 $j
  done
done
