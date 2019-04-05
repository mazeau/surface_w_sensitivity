export RMGpy=$HOME/Code/RMG-Py
find . -name run_ft.sh -execdir sh -c "sbatch run_ft.sh" \;
