import os
import shutil

array = os.listdir('../../linear-scaling-tests/binding_energies/')

# get the species dictionaries
for x in array:
    try:
        shutil.copy2('../../linear-scaling-tests/binding_energies/' + x + '/chemkin/species_dictionary.txt',
                 './linearscaling/species_dictionary.txt' + x)
    except:
        print 'cannot find species_dictionary for %s'%(x)
    try:
        shutil.copy2('../../linear-scaling-tests/binding_energies/' + x + '/cantera/chem.cti',
                 './linearscaling/chem.cti' + x)
    except:
        print 'cannot find cantera file for %s'%(x)
