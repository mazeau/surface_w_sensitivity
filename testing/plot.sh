#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --partition=general,west
#SBATCH --exclude=c5003
#SBATCH --mem=60Gb
#SBATCH --time=2:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=4000 --to notebook --execute plots2.ipynb --output=plotsdone.ipynb
