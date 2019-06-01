export RMGpy=/scratch/westgroup/mazeau/Cat/RMG-Py
#find . -name run.sh -execdir sh -c "sbatch run.sh" \;
find . -name runparallel.sh -execdir sh -c "sbatch runparallel.sh" \;

