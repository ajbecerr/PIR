#!/bin/sh

for i in {1..8}
do
  for j in {1..8}
  do 
    sbatch PIR_3_1.sh 0 $i $j
  done
done

for i in {1..8}
do
  for j in {1..8}
  do 
    sbatch PIR_3_1.sh $i 0 $j
  done
done
