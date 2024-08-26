#!/bin/sh

# for i in {0..7}
# do
#     sbatch mpi4qiskit_1.sh 3 100000 $i # sbatch mpi4qiskit_1.sh 3 100000 0 0
# done

# for i in {0..7}
# do
#     sbatch mpi4qiskit_1.sh 3 10000 $i # sbatch mpi4qiskit_1.sh 3 100000 0 0
# done

# for i in {0..7}
# do
#     sbatch mpi4qiskit_1.sh 3 1000 $i # sbatch mpi4qiskit_1.sh 3 100000 0 0
# done

# for i in {0..7}
# do
#     sbatch mpi4qiskit_1.sh 3 100 $i # sbatch mpi4qiskit_1.sh 3 100000 0 0
# done

# for i in {0..7}
# do
#     sbatch mpi4qiskit_1.sh 3 10 $i # sbatch mpi4qiskit_1.sh 3 100000 0 0
# done

for i in {0..7}
do
    sbatch mpi4qiskit_1.sh 3 1 $i # sbatch mpi4qiskit_1.sh 3 100000 0 0
done