#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH -n1
#SBATCH --output=output.log
#SBATCH --partition=west,short
#SBATCH --exclude=c5003
#SBATCH --mem=40Gb
#SBATCH --time=2:00:00

#jupyter nbconvert --ExecutePreprocessor.timeout=4000 --to notebook --execute plots2.ipynb --output=plotsdone.ipynb
source activate rmg_env
python plots2.py
