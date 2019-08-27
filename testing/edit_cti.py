# replace reversible oxygen reaction with forward and reverse with coverage

import os
import re

array = os.listdir('./linearscaling')
files = ['./linearscaling/' + x for x in array]

f = open('chem_annotated.cti', mode='r')
g = open('chem_annotated_tmp.cti', mode='a')

file = f.readlines()
for line in file:
    # if re.search(r'X\(1\) + X\(1\) + O2\(3\) <=', line):
    if re.search(r'X[(]1[)]\s\+\sX[(]1[)]\s\+\sO2[(]3[)]', line) is not None:
        line = re.sub(r'<=', r'=', line)
        g.write(line)
    else:
        g.write(line)
g.write('surface_reaction( "OX(20) + OX(20) => O2(3) + X(1) + X(1)", ')
g.write('Arrhenius(3.70000E+21, 0, 235500, ')
g.write("coverage = ['OX(20)', 0.0, 0.0, -188300.0]) )")
f.close()
g.close()

os.remove('chem_annotated.cti')
os.rename('chem_annotated_tmp.cti', 'chem_annotated.cti')

for x in files:
    f = open(x + '/chem_annotated.cti', 'r')
    g = open(x + '/chem_annotated_tmp.cti', mode='a')
    file = f.readlines()
    for line in file:
        if re.search(r'X[(]1[)]\s\+\sX[(]1[)]\s\+\sO2[(]3[)]', line) is not None:
            line = re.sub(r'<=', r'=', line)
            g.write(line)
        else:
            g.write(line)
    g.write('surface_reaction( "OX(20) + OX(20) => O2(3) + X(1) + X(1)", ')
    g.write('Arrhenius(3.70000E+21, 0, 235500, ')
    g.write("coverage = ['OX(20)', 0.0, 0.0, -188300.0]))")
    f.close()
    g.close()

    os.remove(x + '/chem_annotated.cti')
    os.rename(x + '/chem_annotated_tmp.cti', x + '/chem_annotated.cti')
