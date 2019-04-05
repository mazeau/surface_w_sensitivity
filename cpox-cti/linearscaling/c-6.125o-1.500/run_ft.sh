#!/bin/bash
#SBATCH --job-name=ft_sensitivity
#SBATCH --error=ft_error.log
#SBATCH -n1
#SBATCH --output=ft_output.log
#SBATCH --exclusive
#SBATCH --partition=general
#SBATCH --mem=120Gb
#SBATCH --time=10:00:00

jupyter nbconvert --ExecutePreprocessor.timeout=40000 --to notebook --execute copyme-fixed-temp-profile.ipynb --output=ft-alldone.ipynb
