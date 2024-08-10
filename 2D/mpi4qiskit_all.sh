#!/bin/sh
# sbatch mpi4qiskit_1.sh 3 100000 0 0
# for i in {0..7}
# do
#     for j in {0..7}
#     do
#         sbatch mpi4qiskit_1.sh 3 100000 $i $j
#     done
# done
# for i in {0..15}
# do
#     for j in {0..15}
#     do
#         sbatch mpi4qiskit_1.sh 4 100000 $i $j
#     done
# done
for i in {0..31}
do
    for j in {0..31}
    do
        sbatch mpi4qiskit_1.sh 5 100000 $i $j
    done
done
# for i in {0..63}
# do
#     for j in {0..63}
#     do
#         sbatch mpi4qiskit_1.sh 6 100000 $i $j
#     done
# done
# for i in {0..127}
# do
#     for j in {0..127}
#     do
#         sbatch mpi4qiskit_1.sh 7 100000 $i $j
#     done
# done