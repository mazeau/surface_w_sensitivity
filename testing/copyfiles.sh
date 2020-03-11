#!/bin/bash
#SBATCH --job-name=copy
#SBATCH --error=error.log
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --output=output.log
#SBATCH --exclude=c[5003]
#SBATCH --exclusive
#SBATCH -c 56
#SBATCH --partition=short,large,express
#SBATCH --time=0:30:00

source activate rmg_env
python scratchfiles.py
