#!/bin/bash
#SBATCH --qos=debug
#SBATCH --constraint=knl
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=15
#SBATCH --time=0:02:00

source activate rmg_env
python copyme-parallel.py
