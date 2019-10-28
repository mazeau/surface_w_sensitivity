"""
This example is from doi:10.1021/acscatal.7b03205, Huber et al.

ethylene dimerization and oligomerization to 1 butene
"""
# load a bunch of stuff
import cantera as ct
import numpy as np
import scipy
import pylab
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.pyplot import cm
from matplotlib.ticker import NullFormatter, MaxNLocator, LogLocator
plt.switch_backend('agg')  # needed for saving figures
import csv
from pydas.dassl import DASSL
import os

import re
import operator
import pandas as pd
import pylab
from cycler import cycler
import seaborn as sns
import os
import multiprocessing
import sys

# this chemkin file is from the cti generated by rmg
gas = ct.Solution('./chem_annotated.cti', 'gas')
surf = ct.Interface('./chem_annotated.cti', 'surface1', [gas])

print("This mechanism contains {} gas reactions and {} surface reactions".format(gas.n_reactions, surf.n_reactions))

i_c2h4 = gas.species_index('C2H4(2)')
i_nheptane = gas.species_index('n-heptane')
i_c4h8_1 = gas.species_index('C4H8-1(3)')  # 1 butene
i_c4h8_2 = gas.species_index('C4H8-2(4)')  # 2 butene
# i_c6h12_1 = gas.species_index('C6H12-1(7)')
# i_c6h12_2 = gas.species_index('C6H12-2(8)')
# i_c6h12_3 = gas.species_index('C6H12-3(9)')
# i_c6h12_1_3 = gas.species_index('C6H12-1-3(10)')
# i_c6h12_2_3 = gas.species_index('C6H12-2-3(11)')

# unit conversion factors to SI
mm = 0.001
cm = 0.01
ms = mm
minute = 60.0

cat_area_per_vol = 5.9e8  # in m-1


def semibatch(gas, surf, temp, pressure, volume, mol_in, verbose=False, sens=False):
    """

    :param gas: from cti
    :param surf: from cti
    :param temp: Kelvin
    :param pressure: Pa
    :param volume: m^3
    :param mol_in: ratio
    :param verbose:
    :param sens:
    :return:
    """
    cat_area = cat_area_per_vol * volume

    c2h4, nh = mol_in
    c2h4 = str(c2h4)
    nh = str(nh)
    X = str('C2H4(2):' + c2h4 + ', n-heptane:' + nh)  # gas concentrations

    surf.TP = temp, pressure
    surf.coverages = 'X(1):1.0'

    # create an upstream reservoir that will supply the reactor. The temperature
    #  and pressure of the upstream reservoir of pure ethylene
    gas.TPX = temp, pressure, 'C2H4(2):1'
    upstream = ct.Reservoir(gas)
    exhaust = ct.Reservoir(gas)

    # set the gas to the specified input concentrations
    gas.TPX = temp, pressure, X

    # Now create the reactor object with a differnet initial state.  Turn energy off
    # so the temperature stays at its initial value
    r = ct.IdealGasReactor(gas, energy='off')

    # Set its volume. In this problem, the reactor volume is fixed, so
    # the initial volume is the volume at all later times.
    r.volume = volume

    # Add the reacting surface to the react or. The area is set to the desired
    # catalyst area in the reactor.
    rsurf = ct.ReactorSurface(surf, r, A=cat_area)

    # create a valve to feed in ethylene from the reservoir to the reactor if the pressure drops
    pressureRegulator = ct.Valve(upstream=upstream,
                                 downstream=r,
                                 K=1e-3)  # CVODES at 2e-2 when the second valve is on

    # trying to keep pressure from building up
    pressureRegulator2 = ct.Valve(upstream=r,
                                  downstream=exhaust,
                                  K=1e-4)

    sim = ct.ReactorNet([r])
    sim.max_err_test_fails = 12

    # set relative and absolute tolerances on the simulation
    sim.rtol = 1.0e-10
    sim.atol = 1.0e-20

    # rxn_time = np.linspace(1E-5, np.log10(3600), 1000001)  # from 0s to 3600s (1 hour)
    rxn_time = np.logspace(-5, np.log10(3600), 1000001)  # from 0s to 3600s (1 hour), log spacing
    gas_mole_fracs = np.zeros([gas.n_species, len(rxn_time)])
    surf_site_fracs = np.zeros([surf.n_species, len(rxn_time)])
    p = np.zeros(len(rxn_time))
    temperature = np.zeros(len(rxn_time))
    v = np.zeros(len(rxn_time))

    if verbose is True:
        print('     time        X_C2H4       X_C4H8-1')

    surf.set_multiplier(1.0)
    if sens is not False:
        surf.set_multiplier(1.0 + sens[0], sens[1])
    for i in range(len(rxn_time)):
        time = rxn_time[i]  # define time in the reactor
        sim.advance(time)  # Advance the simulation to next set time
        # p[i] = gas.P / ct.one_atm
        p[i] = gas.P / 1e6  # MPa
        gas_mole_fracs[:, i] = gas.X
        surf_site_fracs[:, i] = surf.coverages
        temperature[i] = gas.T
        v[i] = r.volume

        if verbose is True:
            if not i % 1000:
                print('  {0:10f}  {1:10f} '.format(time, *gas[
                    'C2H4(2)', 'C4H8-1(3)'].X))

        # make reaction diagrams
        out_dir = 'rxnpath'
        os.path.exists(out_dir) or os.makedirs(out_dir)
        elements = ['H', 'C']
        """
        Times to generate rxnpath diagrams (times_of_interest):
        [0, 116873, 233746, 350619, 467492, 584365, 792183, 909056, 1000000]

        corresponds to:
         - at the beginning of time, 1e-5 seconds
         - just after 1e-4 seconds
         - just after 1e-3 seconds
         - just after 1e-2 seconds
         - just after 1e-1 seconds
         - just after 1 second
         - just after 1 minute
         - just after 10 minutes
         - at an hour
         
        was running [0, 1e2, 1e3, 1e4, 1e5, 1e6] before
        """
        times_of_interest = [0, 116873, 233746, 350619, 467492, 584365, 792183, 909056, 1000000]
        if sens is False:
            for l in times_of_interest:
                if i == l:
                    time = '{:0.1e}'.format(rxn_time[l])

                    diagram = ct.ReactionPathDiagram(surf, 'X')
                    diagram.title = 'rxn path'
                    diagram.label_threshold = 1e-9
                    dot_file = out_dir + '/x-' + time + '.dot'
                    img_file = out_dir + '/x-' + time + '.png'
                    img_path = os.path.join(out_dir, img_file)
                    diagram.write_dot(dot_file)
                    os.system('dot {0} -Tpng -o{1} -Gdpi=200'.format(dot_file, img_file))

                    for element in elements:
                        diagram = ct.ReactionPathDiagram(surf, element)
                        diagram.title = element + 'rxn path'
                        diagram.label_threshold = 1e-9
                        dot_file = out_dir + '/surf-' + time + '-' + element + '.dot'
                        img_file = out_dir + '/surf-' + time + '-' + element + '.png'
                        img_path = os.path.join(out_dir, img_file)
                        diagram.write_dot(dot_file)
                        os.system('dot {0} -Tpng -o{1} -Gdpi=200'.format(dot_file, img_file))
        else:
            pass


    # check to see if the pressure stays the same throughout
    maxPressureRiseAllowed = 1e-2  # MPa
    pressureDifferential = np.amax(p) - np.amin(p)
    if abs(pressureDifferential) > maxPressureRiseAllowed:
        print("WARNING: Non-trivial pressure change of {0:3f} MPa in reactor!".format(pressureDifferential))

    surf.set_multiplier(1.0)  # resetting things, just incase sensitivity was running
    return gas_mole_fracs, surf_site_fracs, rxn_time, p


def plot(data, log=False):
    gas_mole_fracs, surf_site_fracs, rxn_time, pressure = data

    #Plot out simulations results
    fig = pylab.figure(dpi=300, figsize=(12, 8))
    gs = gridspec.GridSpec(2, 1)
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    y_min = 1E-2

    for i in range(gas.n_species):
        if np.max(gas_mole_fracs[i,:]) > y_min:
            if log is True:
                ax0.loglog(rxn_time, gas_mole_fracs[i, :], label=gas.species_name(i))
                ax0.set_xlim(1e-5, max(rxn_time))
                ax0.set_ylim(1e-4, 2)
            else:
                # ax0.semilogy(rxn_time, gas_mole_fracs[i,:], label=gas.species_name(i) )
                ax0.plot(rxn_time, gas_mole_fracs[i, :], label=gas.species_name(i))
                ax0.set_xlim(0., max(rxn_time))
                ax0.set_ylim(y_min, 1.1)

    for i in range(surf.n_species):
        if np.max(surf_site_fracs[i,:]) > y_min:
            if log is True:
                ax1.loglog(rxn_time, surf_site_fracs[i, :], label=surf.species_name(i))
                ax1.set_xlim(1e-5, max(rxn_time))
                ax1.set_ylim(1e-4, 2)
            else:
                # ax1.semilogy(rxn_time, surf_site_fracs[i,:], label=surf.species_name(i) )
                ax1.plot(rxn_time, surf_site_fracs[i, :], label=surf.species_name(i))
                ax1.set_xlim(0.,max(rxn_time))
                ax1.set_ylim(y_min, 1.1)

    # putting legend on the outside of the plot for now because it's really long
    box = ax0.get_position()
    ax0.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    ax0.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=2, shadow=False,)
    box2 = ax1.get_position()
    ax1.set_position([box2.x0, box2.y0, box2.width * 0.5, box2.height])
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=2, shadow=False,)

    ax0.set_ylabel("gas-phase mole fraction", fontsize=14)
    ax0.set_ylim(y_min, 1.)

    # ax0.set_xlabel("Time(s)", fontsize=20)
    ax1.set_ylabel("surface site fraction", fontsize=14)
    #ax0.xaxis.set_major_locator(MaxNLocator(6))
    #ax0.yaxis.set_major_locator(LogLocator(base=10.0, numticks=3))
    #ax0.tick_params(axis='both', which='major', labelsize=10)
    ax1.set_xlabel("Time(s)", fontsize=14)
    if log is True:
        fig.savefig('./figures/batch-log.pdf', bbox_inches='tight')
    else:
        fig.savefig('./figures/batch.pdf', bbox_inches='tight')
    plt.close()


#######################################################################
# Input Parameters
#######################################################################

t_in = 423.15  # K, uniform temperature profile
gas_names = gas.species_names
surf_names = surf.species_names

p = 35  # bar or 3.5 MPa
pressure = p * 1e5  # Pa
volume = 0.3e-3  # m^3

f_ethylene = 2
f_nheptane = 1
ratio_in = [f_ethylene, f_nheptane]
print('Starting model simulation')
a = semibatch(gas, surf, t_in, pressure, volume, ratio_in)
print('Finished model simulation')
gas_mole_fracs, surf_site_fracs, rxn_time, pressure1 = a
plot(a, log=True)
plot(a)

plt.semilogx(rxn_time, pressure1)
plt.savefig('pressure.pdf')

import rmgpy
import rmg

species_dict = rmgpy.data.kinetics.KineticsLibrary().getSpecies('species_dictionary.txt')
keys = species_dict.keys()

# get the first listed smiles string for each molecule
smile = []
for s in species_dict:
    smile.append(species_dict[s].molecule[0])
    if len(species_dict[s].molecule) is not 1:
        print 'There are %d dupllicate smiles for %s:' % (len(species_dict[s].molecule), s)
        for a in range(len(species_dict[s].molecule)):
            print '%s' % (species_dict[s].molecule[a])

# translate the molecules from above into just smiles strings
smiles = []
for s in smile:
    smiles.append(s.toSMILES())
names = dict(zip(keys, smiles))

translated_gas_names = []
for x in gas_names:
    for key, smile in names.iteritems():
        x = re.sub(re.escape(key), smile, x)
    translated_gas_names.append(x)


def carbon_ct_amounts(gas_mole_fracs):
    # sensitivity reference at the end of an hour
    # paper reported in wt %, so I will as well

    mw = gas.molecular_weights
    gas_out = gas_mole_fracs[:, -1]  # gas at the end of time
    amts = gas_out * mw  # multiplying to get product weights

    carbon_count_amts = []
    num_carbons = set()  # create a list of unique number of carbons in a species

    for x in gas.species():
        carbon = x.composition.get('C')  # get number of carbons
        index = gas.species_index(str(x.name))  # get its index, just to make sure
        carbon_count_amts.append([carbon, translated_gas_names[index], amts[index], gas_out[index]])
        num_carbons.add(carbon)

    return carbon_count_amts


def selectivities(carbon_count_amts):
    # get wt % selectivites as shown in Table 2 the paper doi:10.1016/j.jcat.2014.12.027
    # sort species by number of Cs, as shown in the paper
    C10 = 0.  # product weights of species with 10 or more carbons
    C8 = 0.
    C6 = 0.
    C4 = 0.
    # n-heptane was not included, and neither was methane (would still be a gas at -20 C)
    # selectivity in the paper had C4 to C10+ selectivities add up to 100%
    for x in carbon_count_amts:
        if x[0] == 4.0:
            C4 += x[2]
        elif x[0] == 6.0:
            C6 += x[2]
        elif x[0] == 8.0:
            C8 += x[2]
        elif x[0] >= 10.:
            C10 += x[2]

    tot_prod = C4 + C6 + C8 + C10
    C4_sel = C4 / tot_prod
    C6_sel = C6 / tot_prod
    C8_sel = C8 / tot_prod
    C10_sel = C10 / tot_prod

    # 1-butene weight selectivity
    for x in carbon_count_amts:
        # if x[1] == 'C4H8-1(3)':
        #     butene1_sel = x[2] / tot_prod
        if x[1] == 'C=CCC':  # incase the file is in SMILES
            butene1_sel = x[2] / tot_prod

    # getting mol percent, from Table 4
    C4_mol = []
    C6_mol = []
    for x in carbon_count_amts:
        if x[0] == 4.0:
            C4_mol.append([x[1], x[3]])
        if x[0] == 6.0:
            C6_mol.append([x[1], x[3]])

    C4_mol_percents = []
    t = 0.
    for x in C4_mol:
        t += x[1]
    for x in C4_mol:
        percent = x[1] / t
        C4_mol_percents.append([x[0], percent])

    C6_mol_percents = []
    t = 0.
    for x in C6_mol:
        t += x[1]
    for x in C6_mol:
        percent = x[1] / t
        C6_mol_percents.append([x[0], percent])

    return C4_sel, C6_sel, C8_sel, C10_sel, butene1_sel, C4_mol_percents, C6_mol_percents


def export(data, title, column_headers=False, outdir=False):
    """
    export data as a csv file
    :param data: the data
    :param title: the string title of the csv
    :param column_headers: list of strings for column names
    :param outdir: string output directory (probably a folder name).  don't include end slash
    :return:
    """
    k = (pd.DataFrame.from_dict(data=data, orient='columns'))

    header = False
    if column_headers is not False:
        k.columns = column_headers
        header = True

    title = str(title)

    if outdir is not False:
        out_dir = outdir
        os.path.exists(out_dir) or os.makedirs(out_dir)
        out_dir = out_dir + '/'

    else:
        out_dir = ''

    k.to_csv(out_dir + title + '.csv', header=header)


# getting the amount of carbons and end gas amounts in weight and mole fraction
carbon_count_amts = carbon_ct_amounts(gas_mole_fracs)
reference_selectivities = selectivities(carbon_count_amts)

# export carbon count amounts to a csv
print('Exporting data to csv')
column_titles = ['Number of Carbons', 'Species', 'End Weight', 'End mol fraction']
export(carbon_count_amts, 'CarbonCount', column_headers=column_titles)


def sensitivities(reference_selectivities, new_selectivities, sens):
    """
    calculate the sensitivities
    :param reference_selectivities: C4_sel_ref, C6_sel_ref, C8_sel_ref, C10_sel_ref, butene1_sel_ref, C4_mol_percents_ref, C6_mol_percents_ref
    :param new_selectivities: C4_sel_ref_new, C6_sel_ref_new, C8_sel_ref_new, C10_sel_ref_new, butene1_sel_ref_new, C4_mol_percents_ref_new, C6_mol_percents_ref_new
    :param [dk, m] the perturbation and reaction number
    :return:
    """
    dk = sens[0]
    m = sens[1]

    sensitivities = []

    # cycle through the reference and new selectivities
    for x in xrange(len(reference_selectivities)):
        if type(reference_selectivities[x]) == list:  # it is either C4 or C6 mol percents
            s = []
            for y in xrange(len(reference_selectivities[x])):
                t = (new_selectivities[x][y][1] - reference_selectivities[x][y][1]) / (reference_selectivities[x][y][1] * dk)
                s.append([reference_selectivities[x][y][0], t])
            sensitivities.append(s)
        else:
            s = (new_selectivities[x] - reference_selectivities[x]) / (reference_selectivities[x] * dk)
            sensitivities.append(s)

    print "%d %s %.3F " % (m, surf.reaction_equations()[m], sensitivities[4])  # print the 1-butene weight selectivity
    # rxn = surf.reaction_equations()[m]
    return sensitivities


# # set the value of the perturbation
# dk = 1.0e-2
# sen = []
# rxns = []
#
# for m in range(surf.n_reactions):
#     sens = [dk, m]
#     b = semibatch(gas, surf, t_in, pressure, volume, ratio_in, sens=sens)
#     gas_mole_fracs_new, surf_site_fracs_new, rxn_time, p2 = b
#
#     new_carbon_count_amts = carbon_ct_amounts(gas_mole_fracs_new)
#     new_selectivities = selectivities(carbon_count_amts)
#
#     sens, rxn = sensitivities(reference_selectivities, new_selectivities, sens)
#     sen.append(sens)  # the last 2 columns are nested lists for C4 and C6 mol percents
#     rxns.append(rxn)


## MULTIPROCESSING ##


def sensworker(m):
    dk = 1.0e-2  # set the value of the perturbation
    sens = [dk, m]
    f_ethylene = 2
    f_nheptane = 1
    ratio_in = [f_ethylene, f_nheptane]
    t_in = 423.15  # K, uniform temperature profile
    p = 35  # bar or 3.5 MPa
    pressure = p * 1e5  # Pa
    volume = 0.3e-3  # m^3

    try:
        b = semibatch(gas, surf, t_in, pressure, volume, ratio_in, sens=sens)
        gas_mole_fracs_new, surf_site_fracs_new, rxn_time, p2 = b

        new_carbon_count_amts = carbon_ct_amounts(gas_mole_fracs_new)
        new_selectivities = selectivities(new_carbon_count_amts)

        sens = sensitivities(reference_selectivities, new_selectivities, sens)
        # sen.append(sens)  # the last 2 columns are nested lists for C4 and C6 mol percents
        # rxns.append(rxn)

        return sens
    except:
        print('Unable to run simulation for %d %s'.format(m, surf.reaction_equations()[m]))
        pass


print('Starting {} sensitivity simulations'.format(surf.n_reactions))
num_threads = multiprocessing.cpu_count()
m_list = []
for x in range(surf.n_reactions):
    m_list.append(x)
rxns = []
for x in range(surf.n_reactions):
    rxns.append(surf.reaction_equations()[x])
pool = multiprocessing.Pool(processes=num_threads)
sen = pool.map(sensworker, m_list, 1)
pool.close()
pool.join()
##########

# translate the surface reactions to SMILES
rxns_translated = []
for x in rxns:
    for key, smile in names.iteritems():
        x = re.sub(re.escape(key), smile, x)
    rxns_translated.append(x)

print('Exporting sensitivity data to a csv')
# first, output the mol percents sensitivities (C4 index 5 and C6 index 6)
output = []
header_titles = ['Reaction']
k = False
for x in xrange(len(sen)):
    mol_percents = sen[x][5]  # species, mol percents
    s = []
    for y in mol_percents:
        s.append(y[1])  # sensitivity of mol percent
        if k is False:
            header_titles.append(y[0])
    s.insert(0, rxns_translated[x])
    output.append(s)
    k = True
export(output, 'C4molpercents', column_headers=header_titles, outdir='sensitivities')

# output the mol percents of C6
output = []
header_titles = ['Reaction']
k = False
for x in xrange(len(sen)):
    mol_percents = sen[x][6]  # species, mol percents
    s = []
    for y in mol_percents:
        s.append(y[1])  # sensitivity of mol percent
        if k is False:
            header_titles.append(y[0])
    s.insert(0, rxns_translated[x])
    output.append(s)
    k = True
export(output, 'C6molpercents', column_headers=header_titles, outdir='sensitivities')

# output everything else that wasn't a list
delete_row = []
for x in xrange(len(reference_selectivities)):
    if type(reference_selectivities[x]) == list:  # it is either C4 or C6 mol percents
        delete_row.append(x)

delete_row = delete_row[::-1]
for row in sen:
    for index in delete_row:
        del row[index]

output = []
for x in xrange(len(sen)):
    y = sen[x]
    y.insert(0, rxns_translated[x])
    output.append(y)
header_titles = ['Reaction', 'C4 selectivity', 'C6 selectivity', 'C8 selectivity', 'C10+ selectivity',
                 '1-Butene selectivity']
export(sen, 'selectivities', column_headers=header_titles, outdir='sensitivities')