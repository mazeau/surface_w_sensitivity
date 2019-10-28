#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --partition=general,west
#SBATCH --exclude=c5003
#SBATCH --mem=10Gb
#SBATCH --time=2:00:00

source activate rmg_env3
python copyme-parallel.py
#python batch.py
