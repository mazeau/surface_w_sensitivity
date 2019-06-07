#!/bin/bash
#SBATCH --qos=regular
#SBATCH --constraint=knl
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=15
#SBATCH --mem-per-cpu=1Gb
#SBATCH --time=1:00:00

source activate rmg_env
python copyme-parallel.py
