import os, glob
import shutil

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

for x in files:
    # copying the copyme file and pasting into each linearscaling folder
    shutil.copy('copyme.ipynb', x)
    shutil.copy('run.sh', x)
    # removing prior error and output logs, as well as old results
    try:
        os.remove(x + '/output.log')
    except:
        pass
    try:
        os.remove(x + '/error.log')
    except:
        pass
    try:
        os.remove(x + '/alldone.ipynb')
    except:
        pass
    # removing past data
    try:
	os.remove(x + '/dict.csv')
    except:
	pass
    try:
	os.remove(x + '/time.txt')
    except:
	pass
    for file in glob.glob(x + "/rxnpath*"):
        os.remove(file)
for file in glob.glob("rxnpath*"):
        os.remove(file)
