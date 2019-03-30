#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --exclusive
#SBATCH --partition=general
#SBATCH --mem=50Gb
#SBATCH --time=2:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=4000 --to notebook --execute plots.ipynb --output=plotsdone.ipynb
