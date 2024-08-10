#!/bin/sh
#SBATCH -N 1
#SBATCH -J 2dSlab
#SBATCH -t 1:00:00
#SBATCH -p patralab
#SBATCH --mem-per-cpu=4g
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=alejandro.becerra@tufts.edu
module load gcc/7.3.0 openmpi/4.0.4
module load anaconda/2021.05
# pip install mpi4py
# pip install pylatexenc
# pip install qiskit
# pip install qiskit_aer
# pip install typing_extensions --upgrade
var=$((2**($1-2)))
mkdir -p $1
python Pauli.py $1
mpirun --oversubscribe -np $var python mpi4qiskit_1.py $1 $2 $3 $4
python AggStore.py $1 $3 $4