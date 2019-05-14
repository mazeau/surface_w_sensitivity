#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH --partition=west,general
#SBATCH --exclude=c5003
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=3Gb

source activate rmg_env3
python copyme-parallel.py
#jupyter nbconvert --ExecutePreprocessor.timeout=40000 --to notebook --execute copyme-parallel.ipynb --output=alldone-parallel.ipynb
