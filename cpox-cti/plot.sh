#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --mem=15Gb
#SBATCH --time=12:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=40000 --to notebook --execute plots.ipynb --output=plotsdone.ipynb
