#!/bin/bash
#SBATCH --qos=regular
#SBATCH --constraint=knl
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=15
#SBATCH --mem=10Gb
#SBATCH --time=1:00:00
#SBATCH --mail-type=end,fail
#SBATCH --mail-user=mazeau.e@husky.neu.edu

source activate rmg_env
python copyme-parallel.py
