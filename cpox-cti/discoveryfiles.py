import os
import shutil

array = os.listdir('../../linear-scaling-tests/binding_energies/')
species = ['../../linear-scaling-tests/binding_energies/' + x for x in array + '/chemkin/species_dictionary.txt']
chemkin = ['../../linear-scaling-tests/binding_energies/' + x for x in array + '/cantera/chem.cti']

# get the species dictionaries
for x in species:
    shutil.copy2(x, './linearscaling/')