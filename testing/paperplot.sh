#!/bin/bash
#SBATCH --job-name=paperplot
#SBATCH --error=error.log
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --output=output.log
#SBATCH --exclude=c[5003]
#SBATCH -c 15
#SBATCH --partition=short,large,express
#SBATCH --time=0:30:00

source activate rmg_env
python paperplots.py
