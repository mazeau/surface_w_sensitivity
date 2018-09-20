#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH -n1
#SBATCH --mem=10Gb
#SBATCH --time=3:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=9999 --to notebook --execute copyme.ipynb --output=alldone.ipynb
