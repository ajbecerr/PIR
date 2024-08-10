#!/bin/sh
for i in {0..7}
do
    for j in {0..7}
    do
        sbatch mpi4qiskit_1.sh 3 100000 $i $j
    done
done
# sbatch mpi4qiskit_1.sh 3 100000 0 0