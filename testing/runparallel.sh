#!/bin/bash
#SBATCH --job-name=methanol
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH -n 1
#SBATCH -N 1
#SBATCH --partition=west,general,test,interactive
#SBATCH --exclude=c5003
#SBATCH -c 6
#SBATCH --mem-per-cpu=4Gb
#SBATCH --time=00:10:00

source activate rmg_env
python copyme-parallel.py
#python copymetest.py
