#!/bin/bash
#SBATCH --job-name=plot
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH -N 1
#SBATCH --output=output.log
#SBATCH --exclude=c[5003]
#SBATCH -c 56
#SBATCH --partition=short,large, express
#SBATCH --time=0:30:00

source activate rmg_env
python plots2.py
