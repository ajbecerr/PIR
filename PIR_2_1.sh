#!/bin/sh
#SBATCH -N 1
#SBATCH -J 2dSlab
#SBATCH -t 24:00:00
#SBATCH -p pbatch
#SBATCH --mail-type=ALL
#SBATCH -A sunyb
#SBATCH --mail-user=ajbecerr@buffalo.edu
module load python
python PIR_2.py $1 $2 $3 $4 $5
