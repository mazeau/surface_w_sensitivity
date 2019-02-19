import os
import shutil

array = os.listdir('../../../linear-scaling-tests/cpox/binding_energies/')
#array = os.listdir('/scratch/westgroup/mazeau/linear-scaling-tests/cpox/binding_energies/')
print array

# get the species dictionaries
for x in array:
    try:
        shutil.copy2('../../../linear-scaling-tests/cpox/binding_energies/' + x + '/chemkin/species_dictionary.txt','./linearscaling/' + x + '/species_dictionary.txt')
    except:
        print 'cannot find species_dictionary for %s'%(x)
    try:
        shutil.copy2('../../../linear-scaling-tests/cpox/binding_energies/' + x + '/cantera/chem.cti','./linearscaling/' + x + '/chem.cti')
    except:
        print 'cannot find cantera file for %s'%(x)
