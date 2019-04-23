import os, glob
import shutil

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

for x in files:
    # copying the copyme file and pasting into each linearscaling folder
    shutil.copy('copyme.ipynb', x)
    shutil.copy('run.sh', x)
    #shutil.copy('copyme-fixed-temp-profile.ipynb', x)
    #shutil.copy('run_ft.sh' ,x)
