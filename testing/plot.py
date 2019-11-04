from matplotlib import pyplot as plt
import matplotlib
import seaborn as sns
sns.set_style("ticks")
sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.0})

import os
import re
import pandas as pd
import numpy as np
import shutil
import subprocess
import multiprocessing
import re
import cantera as ct

carbon_range = (-10, -2)
hydrogen_range = (-3.5, -1.5)
grid_size = 9
mesh = np.mgrid[carbon_range[0]:carbon_range[1]:grid_size * 1j,
       hydrogen_range[0]:hydrogen_range[1]:grid_size * 1j]

with sns.axes_style("whitegrid"):
    plt.axis('square')
    plt.xlim(carbon_range)
    plt.ylim(hydrogen_range)
    plt.yticks(np.arange(-3.5, -1, 0.5))
plt.show()

experiments = mesh.reshape((2,-1)).T

with sns.axes_style("whitegrid"):
    plt.axis('square')
    plt.xlim(carbon_range)
    plt.ylim(hydrogen_range)
    plt.plot(*experiments.T, marker='o', linestyle='none')

extent = carbon_range + hydrogen_range

# Because the center of a corner pixel is in fact the corner of the grid# Becaus
# we want to stretch the image a little
c_step = mesh[0,1,0]-mesh[0,0,0]
o_step = mesh[1,0,1]-mesh[1,0,0]
carbon_range2 = (carbon_range[0]-c_step/2, carbon_range[1]+c_step/2)
oxygen_range2 = (oxygen_range[0]-c_step/2, oxygen_range[1]+c_step/2)
extent2 = carbon_range2 + oxygen_range2


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
            butene1_yield = x[2]

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

    return C4_sel, C6_sel, C8_sel, C10_sel, butene1_sel  # C4_mol_percents, C6_mol_percents


def import_data(file_location=False):
    """
    This imports CarbonCount.csv from the original simulation
    """
    if file_location is False:
        data = pd.read_csv('./CarbonCount.csv')
        data = data.get_values()
    else:
        try:
            data = pd.read_csv('./linearscaling/' + file_location + '/CarbonCount.csv')
            data = data.get_values()
        except:
            print(file_location + '/CarbonCount.csv does not exist')
            return None

    # data = data.get_values()
    return selectivities(data)


# For close packed surfaces from
# Abild-Pedersen, F.; Greeley, J.; Studt, F.; Rossmeisl, J.; Munter, T. R.; Moses, P. G.; Skulason, E.; Bligaard, T.;
# Norskov, J. K. Scaling Properties of Adsorption Energies for Hydrogen-Containing Molecules on Transition-Metal
# Surfaces. Phys. Rev. Lett. 2007, 99 (1), 016105 DOI: 10.1103/PhysRevLett.99.016105.
abildpedersen_energies = { # Carbon, then Hydrogen.  Hydrogen calculated from Katrin's data
'Ru': ( -6.397727272727272, -2.89411110),
'Rh': ( -6.5681818181818175, -2.83800775),
# 'Ni': ( -6.045454545454545, -4.711681807593758),
'Ir': ( -6.613636363636363, -2.67453337),
'Pd': ( -6, -2.90619315),
'Pt': ( -6.363636363636363, -2.74272356),
# 'Cu': ( -4.159090909090907, -2.57906515),
# 'Ag': ( -2.9545454545454533, -2.11693383),
# 'Au': ( -3.7499999999999973, -2.15944428),
}


def lavaPlot(overall_rate, title, axis=False, folder=False, interpolation=True):
    """
    overall rate data to plot
    title is a string for what definition is used
    to normalize colors across many plots, False doesn't normalize axes
    folder specifies where to save the images
    interpolation as false just plots boxes
    """
#     df = pd.DataFrame(index=np.unique(o_s), columns=np.unique(c_s))
#     print df
#     for c, o, t in zip(c_s, o_s, overall_rate):
#         df[c][o] = t
#     a = []
#     for i in df.values:
#         a = a + list(i)
    overall_rate = np.array(overall_rate)
#     rates = 1./np.array(a)
    rates = overall_rate

    rates_grid = np.reshape(rates, (grid_size,grid_size))
    for i in range(0,8):  # transpose by second diagnol
        for j in range(0, 8 - i):
            rates_grid[i][j], rates_grid[8 - j][8 - i] = rates_grid[8 - j][8 - i], rates_grid[i][j]
    if axis is False:  # no normalizing
        if interpolation is True:
            plt.imshow(rates_grid, origin='lower',
                       interpolation='spline16',
                       extent=extent2, aspect='equal', cmap="Spectral_r",)
        else:
            plt.imshow(rates_grid, origin='lower',
                       extent=extent2, aspect='equal', cmap="Spectral_r",)
    else:
        if interpolation is True:
            plt.imshow(rates_grid, origin='lower',
                       interpolation='spline16',
                       extent=extent2, aspect='equal', cmap="Spectral_r",
                       vmin=axis[0], vmax=axis[1], )
        else:
            plt.imshow(rates_grid, origin='lower',
                       extent=extent2, aspect='equal', cmap="Spectral_r",
                       vmin=axis[0], vmax=axis[1], )

    for metal, coords in abildpedersen_energies.iteritems():
        color = {'Ag': 'k', 'Au': 'k', 'Cu': 'k', 'Ru': 'k', 'Rh': 'k', 'Ir': 'k', 'Pd': 'k', 'Pt': 'k'}.get(metal, 'k')
        plt.plot(coords[0], coords[1], 'o' + color)
        plt.text(coords[0], coords[1] - 0.1, metal, color=color)
    plt.xlim(carbon_range)
    plt.ylim(oxygen_range)
    plt.yticks(np.arange(-3.5, -1, 0.5))
    plt.xlabel('$\Delta E^C$ (eV)')
    plt.ylabel('$\Delta E^H$ (eV)')
    #     plt.title(str(title))
    plt.colorbar()
    out_dir = 'lsr'
    os.path.exists(out_dir) or os.makedirs(out_dir)
    if folder is False:
        plt.savefig(out_dir + '/' + str(title) + '.pdf', bbox_inches='tight')
    else:
        os.path.exists(out_dir + '/' + str(folder)) or os.makedirs(out_dir + '/' + str(folder))
        plt.savefig(out_dir + '/' + str(folder) + '/' + str(title) + '.pdf', bbox_inches='tight')
    plt.show()  # comment out to save fig


array = os.listdir('./linearscaling/')
array = sorted(array)

# for plotting
c_s = []
o_s = []
for x in array:
    _, c, o = x.split("-")
    c = c[:-1]
    c = -1 *float(c)
    o = -1* float(o)
    c_s.append(c)
    o_s.append(o)

# sens_types = ['Number of Carbons', 'Species', 'End Weight', 'End mol fraction']
sens_types = ['C4 Wt Selectivity', 'C6 Wt Selectivity', 'C8 Wt Selectivity', 'C10 Wt Selectivity', '1-Butene Wt Selectivity']

all_data = []
for f in array:
    all_data.append(import_data(file_location=f))

# to normalize colors across ratios
spans = []
for m in range(len(all_data[0])):  # for each sens definition
    all_sens_data = []
    for y in range(len(all_data)):
        # y has len 81 and is each of the lsr binding energies
        # the last number is the type of sensitivity definition and is 0-12
        all_sens_data.append(all_data[y][m])
    vmax = max(all_sens_data)
    vmin = min(all_sens_data)
#     print all_sens_data
    spans.append([vmin, vmax])
    # print sens_types[m], vmin, vmax


for z in range(len(all_data)):
    ans = all_data[z]
    for s in range(len(ans[0])):
        data_to_plot = []
        for x in range(len(ans)):
            data_to_plot.append(ans[x][s])
        title = sens_types[s]
        lavaPlot(data_to_plot, title, axis=spans[s], folder='base_no_interpolation', interpolation=False)

