#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --exclusive
#SBATCH --partition=general
#SBATCH --mem=20Gb
#SBATCH --time=4:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=40000 --to notebook --execute copyme.ipynb --output=alldone.ipynb
