#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --exclusive
#SBATCH --partition=short,west
#SBATCH --mem=50Gb
#SBATCH --time=24:00:00

source activate rmg_env
python plots2.py
#jupyter nbconvert --ExecutePreprocessor.timeout=4000 --to notebook --execute plots.ipynb --output=plotsdone.ipynb
