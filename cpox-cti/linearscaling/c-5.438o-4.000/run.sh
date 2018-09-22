#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --mem=10Gb
#SBATCH --time=5:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=9999 --to notebook --execute copyme.ipynb --output=alldone.ipynb
