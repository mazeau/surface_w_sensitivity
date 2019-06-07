#!/bin/bash
#SBATCH --qos=debug
#SBATCH --constraint=knl
#SBATCH --job-name=sensitivity
#SBATCH --error=error.log
#SBATCH --output=output.log
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=15
#SBATCH --mem=5Gb
#SBATCH --time=0:20:00
#SBATCH --mail-type=begin,end,fail
#SBATCH --mail-user=mazeau.e@husky.neu.edu

source activate rmg_env
python copyme-parallel.py
