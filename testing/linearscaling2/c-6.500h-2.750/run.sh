#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --output=output.log
#SBATCH --partition=gpu,west,general,fullnode
#SBATCH --exclude=c5003
#SBATCH --exclusive
#SBATCH --mem-per-cpu=4Gb
#SBATCH --time=24:00:00

source activate rmg_env3
#python copyme-parallel.py
python batch2.py
