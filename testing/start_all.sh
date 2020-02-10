export RMGpy=/scratch/westgroup/mazeau/Cat/RMG-Py
#find . -name run.sh -execdir sh -c "sbatch run.sh" \;
source activate rmg_env
find . -name runparallel.sh -execdir sh -c "sbatch runparallel.sh" \;

