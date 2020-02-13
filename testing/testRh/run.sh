#!/bin/bash
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH -n 1
#SBATCH --partition=west,short
#SBATCH --exclude=c5003
#SBATCH --mem=30Gb
#SBATCH --time=1:00:00

source activate rmg_env
python paperplots.py
#python copymetest.py
