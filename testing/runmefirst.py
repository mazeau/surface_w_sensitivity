import os, glob
import shutil

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

for x in files:
    # copying the copyme file and pasting into each linearscaling folder
    shutil.copy('copyme-parallel.py', x)
    shutil.copy('runparallel.sh', x)
    #shutil.copy('copyme-fixed-temp-profile.ipynb', x)
    #shutil.copy('run_ft.sh' ,x)
    # removing prior error and output logs, as well as old results
    try:
        os.remove(x + '/output.log')
    except:
        pass
    try:
        os.remove(x + '/error.log')
    except:
        pass
    for file in glob.glob(x + '/figures/*.pdf'):  # remove old plots
        os.remove(file)
    for file in glob.glob(x + '/rxnpath/rxnpath*'):  # remove old rxn path diagrams
        os.remove(file)
    for file in glob.glob(x + '/sensitivities/*.csv'):  # remove old sensitivities
        os.remove(file)
    for file in glob.glob(x + '/*.csv'):  # remove old conversions and selectivities csv
        os.remove(file)

#for file in glob.glob('/figures/*.pdf'):
#    os.remove(file)
#for file in glob.glob('/rxnpath/rxnpath*'):
#    os.remove(file)

# deleting old lsr plots and sensitivities
# for file in glob.glob('lsr/base_no_interpolation/*.pdf'):
#      os.remove(file)
# for file in glob.glob('lsr/rxnsensitivities_nointerpolation/*.pdf'):
#      os.remove(file)
# for file in glob.glob('lsr/thermosensitivities_nointerpolation/*.pdf'):
#      os.remove(file)
