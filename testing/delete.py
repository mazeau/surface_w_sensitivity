import os, glob
import shutil

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

for x in files:
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
    try:
	os.remove(x + '/alldone_ft.ipynb')
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
    try:
	os.remove(x + '/errors.txt')
    except:
	pass
    for file in glob.glob(x + "/rxnpath*"):
        try:
	    os.remove(file)
	except:
	    pass
    for file in glob.glob(x + "/*.png"):
	os.remove(file)
    for file in glob.glob(x + "/*.csv"):
	os.remove(file)
for file in glob.glob("rxnpath*"):
    os.remove(file)
for file in glob.glob("/*.png"):
    os.remove(file)
for file in glob.glob("/*.csv"):
    os.remove(file)
