#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --partition=test
#SBATCH --exclude=c5003
#SBATCH --mem=20Gb
#SBATCH --time=1:00:00

source activate rmg_env3
#python copyme-parallel.py
python batch.py
