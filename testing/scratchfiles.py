import os
import shutil

array = os.listdir('../../../linear-scaling-tests/cpox2/binding_energies/')
#array = os.listdir('/scratch/westgroup/mazeau/linear-scaling-tests/cpox/binding_energies/')


# get the species dictionaries
for x in array:
    os.path.exists('linearscaling/' + x) or os.makedirs('linearscaling/' + x)
    try:
        shutil.copy2('../../../linear-scaling-tests/cpox2/binding_energies/' + x + '/chemkin/species_dictionary.txt','./linearscaling/' + x + '/species_dictionary.txt')
    except:
        print 'cannot find species_dictionary for %s'%(x)
    try:
        shutil.copy2('../../../linear-scaling-tests/cpox2/binding_energies/' + x + '/cantera/chem_annotated.cti','./linearscaling/' + x + '/chem_annotated.cti')
    except:
        print 'cannot find cantera file for %s'%(x)
try:
    shutil.copy2('../../../linear-scaling-tests/cpox2/base/chemkin/species_dictionary.txt','./species_dictionary.txt')
    shutil.copy2('../../../linear-scaling-tests/cpox2/base/cantera/chem_annotated.cti','./chem_annotated.cti')
except:
    print 'cannot find files for base'
