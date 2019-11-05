export RMGpy=/scratch/westgroup/mazeau/Cat/RMG-Py
#find . -name run.sh -execdir sh -c "sbatch run.sh" \;
source activate rmg_env3
find . -name run.sh -execdir sh -c "sbatch run.sh" \;

