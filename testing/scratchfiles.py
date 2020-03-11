import os
import shutil
import multiprocessing

array = os.listdir('../../../linear-scaling-tests/cpox-nodeutschmann/binding_energies/')

def load(x):
    os.path.exists('linearscaling/' + x) or os.makedirs('linearscaling/' + x)
    try:
        shutil.copy2('../../../linear-scaling-tests/cpox-nodeutschmann/binding_energies/' + x + '/chemkin/species_dictionary.txt','./linearscaling/' + x + '/species_dictionary.txt')
    except:
        print('cannot find species_dictionary for %s'%(x))
    try:
        shutil.copy2('../../../linear-scaling-tests/cpox-nodeutschmann/binding_energies/' + x + '/cantera/chem_annotated.cti','./linearscaling/' + x + '/chem_annotated.cti')
    except:
        print('cannot find cantera file for %s'%(x))

try:
    shutil.copy2('../../../linear-scaling-tests/cpox-nodeutschmann/base/chemkin/species_dictionary.txt','./species_dictionary.txt')
    shutil.copy2('../../../linear-scaling-tests/cpox-nodeutschmann/base/cantera/chem_annotated.cti','./chem_annotated.cti')
except:
    print('cannot find files for base')


def worker(x):
    load(x)

pool = multiprocessing.Pool(processes=56)
data = pool.map(worker, array, 7)
pool.close()
pool.join()
