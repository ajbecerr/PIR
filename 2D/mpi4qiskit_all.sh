#!/bin/sh
# for i in {0..7}
# do
#     for j in {0..7}
#     do
#         sbatch mpi4qiskit_1.sh 3 100000 $i $j # sbatch mpi4qiskit_1.sh 3 100000 0 0
#     done
# done

# for i in {0..15}
# do
#     for j in {0..15}
#     do
#         sbatch mpi4qiskit_1.sh 4 100000 $i $j
#     done
# done

# for i in {0..31}
# do
#     for j in {0..31}
#     do
#         sbatch mpi4qiskit_1.sh 5 100000 $i $j # job_limit exceeded
#     done
# done
# for j in {7..31}
# do
#     sbatch mpi4qiskit_1.sh 5 100000 31 $j
# done

# for i in {0..7}
# do
#     for j in {0..63}
#     do
#         sbatch mpi4qiskit_1.sh 6 100000 $i $j
#     done
# done
# for i in {8..15}
# do
#     for j in {0..63}
#     do
#         sbatch mpi4qiskit_1.sh 6 100000 $i $j
#     done
# done
# for i in {16..23}
# do
#     for j in {0..63}
#     do
#         sbatch mpi4qiskit_1.sh 6 100000 $i $j
#     done
# done
# for i in {24..31}
# do
#     for j in {0..63}
#     do
#         sbatch mpi4qiskit_1.sh 6 100000 $i $j
#     done
# done
# for i in {32..39}
# do
#     for j in {0..63}
#     do
#         sbatch mpi4qiskit_1.sh 6 100000 $i $j
#     done
# done
for i in {40..47}
do
    for j in {0..63}
    do
        sbatch mpi4qiskit_1.sh 6 100000 $i $j
    done
done
# for i in {48..55}
# do
#     for j in {0..63}
#     do
#         sbatch mpi4qiskit_1.sh 6 100000 $i $j
#     done
# done
# for i in {56..63}
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