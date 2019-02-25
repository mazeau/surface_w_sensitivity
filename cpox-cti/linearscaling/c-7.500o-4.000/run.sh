#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --mem=120Gb
#SBATCH --time=24:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=40000 --to notebook --execute copyme.ipynb --output=alldone.ipynb
