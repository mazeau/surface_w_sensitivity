import os
import shutil

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

# copying the copyme file and pasting into each linearscaling folder
for x in files:
    shutil.copy('copyme.ipynb', x)
    shutil.copy('run.sh',x)
