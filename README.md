# This is cpox branch for a 19x19 grid
All things happen in the testing folder.

1. Run whatever in linear-scaling-tests on discovery
2. Run copyfiles.sh to run scratchfiles.py to copy all species dictionaries and cantera files from the most recent run of linear-scaling-tests
3. Run runfirst.sh to run runmefirst.py to make sure runparallel.sh and copyme-parallel.py are up to date as well as remove old outputs from previous trials
4. Run ./start_all.sh to start all simulations

This file level is the "base" case.
The `figures` folder on this level shows the output of the "base" copyme-parallel.py
The `linearscaling` folder is for each C and O binding energy.
Inside each `linearscaling` folder, there exists:
    - `dict_conversions_selectivities` where the output of simulations are stored before any sensitivity stuff takes place (like a base case)
    - an identical copy of `copyme-parallel.py` found up 2 file levels
    - the outputs from the mechanism generation run by RMG
    - another `figures` folder where the figures are all saved
    - a `sensitivities` folder where the sensitivities are all saved

The `fixed-temp` folder is for the imposed temperature profile simulation.
The `rxnpath` folder is where reaction paths would be stored (but stopped working randomly on discovery)

While things are running/queued, run `findsens.py` to see if any sensitivity simulations failed (so I can rerun before everything has finished)

After all simulations have been rerun successfully, run `plots.py` or `plots.ipynb` to generate lsr plots.
All plots will be saved in the `lsr` folder.

The `test` folder is left over for when I was trying to figure out how to get CPOX to run because the cat_area_per_vol was too small, and oxygen would all attach to the surface and just stay there.  This will survive the purge for now.

