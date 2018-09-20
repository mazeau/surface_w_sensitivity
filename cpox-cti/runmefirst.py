import os
import shutil

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

for x in files:
    try:
        # copying the copyme file and pasting into each linearscaling folder
        shutil.copy('copyme.ipynb', x)
        shutil.copy('run.sh', x)
        # removing prior error and output logs, as well as old results
        os.remove('output.log')
        os.remove('error.log')
        os.remove('alldone.ipynb')
    except:
	pass
