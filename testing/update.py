import os, glob
import shutil

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

for x in files:
    # copying the copyme file and pasting into each linearscaling folder
    shutil.copy('copyme-parallel.py', x)
    shutil.copy('runparallel.sh', x)
