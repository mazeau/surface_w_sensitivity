#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH -n1
#SBATCH --mem=10Gb

jupyter nbconvert --to notebook --execute copyme.ipynb --output=alldone.ipynb