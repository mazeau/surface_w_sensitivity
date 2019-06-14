import os
import pandas as pd
import numpy as np

def import_sensitivities(ratio, file_location=False, base=False, thermo=False):
    """
    Ratio is the C/O starting gas ratio
    file_location is the LSR C and O binding energy, fasle to load the base case
    thermo is either False to load reaction sensitivities or True to load thermo sensitivities
    """
    try:
        # load in the sensitivity csv files
        if file_location is False:
            if thermo is False:
                data = pd.read_csv('./sensitivities/' + str(ratio) + 'RxnSensitivity.csv')
            else:
                data = pd.read_csv('./sensitivities/' + str(ratio) + 'ThermoSensitivity.csv')
        else:
            if thermo is False:
                data = pd.read_csv('./linearscaling/' + file_location + '/sensitivities/' + str(ratio) + 'RxnSensitivity.csv')
            else:
                data = pd.read_csv('./linearscaling/' + file_location + '/sensitivities/' + str(ratio) + 'ThermoSensitivity.csv')

        reactions = []  # this is reactions or species
        syngas_selectivity = []
        syngas_yield = []
        co_selectivity = []
        co_yield = []
        h2_selectivity = []
        h2_yield = []
        ch4_conversion = []
        full_oxidation_selectivity = []
        full_oxidation_yield = []
        exit_temp = []
        peak_temp = []
        dist_to_peak_temp = []
        # get the values from the data frame
        for y in range(len(data.get_values())):
            reactions.append(data.get_values()[y][1])
            syngas_selectivity.append(data.get_values()[y][2])
            syngas_yield.append(data.get_values()[y][3])
            co_selectivity.append(data.get_values()[y][4])
            co_yield.append(data.get_values()[y][5])
            h2_selectivity.append(data.get_values()[y][6])
            h2_yield.append(data.get_values()[y][7])
            ch4_conversion.append(data.get_values()[y][8])
            full_oxidation_selectivity.append(data.get_values()[y][9])
            full_oxidation_yield.append(data.get_values()[y][10])
            exit_temp.append(data.get_values()[y][11])
            peak_temp.append(data.get_values()[y][12])
            dist_to_peak_temp.append(data.get_values()[y][13])
        # save as dictionaries
        syngasSel = zip(reactions, syngas_selectivity)
        syngasYield = zip(reactions, syngas_yield)
        coSel = zip(reactions, co_selectivity)
        coYield = zip(reactions, co_yield)
        h2Sel = zip(reactions, h2_selectivity)
        h2Yield = zip(reactions, h2_yield)
        ch4Conv = zip(reactions, ch4_conversion)
        fullOxSel = zip(reactions, full_oxidation_selectivity)
        fullOxYield = zip(reactions, full_oxidation_yield)
        exitT = zip(reactions, exit_temp)
        peakT = zip(reactions, peak_temp)
        distPT = zip(reactions, dist_to_peak_temp)

        return syngasSel, syngasYield, coSel, coYield, h2Sel, h2Yield, ch4Conv, fullOxSel, fullOxYield, exitT, peakT, distPT

    except:  # if it cannot load, it returns None
        if thermo is False:
            print('Cannot find ' + str(ratio) + 'RxnSensitivity.csv for:    ' + file_location)
        else:
            print('Cannot find ' + str(ratio) + 'ThermoSensitivity.csv for: ' + file_location)
        # try loading the reactions from a different ratio to use as placeholders
        try_ratios = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6]
        for r in try_ratios:
            try:
                if file_location is False:
                    if thermo is False:
                        data = pd.read_csv('./sensitivities/' + str(r) + 'RxnSensitivity.csv')
                    else:
                        data = pd.read_csv('./sensitivities/' + str(r) + 'ThermoSensitivity.csv')
                else:
                    if thermo is False:
                        data = pd.read_csv('./linearscaling/' + file_location + '/sensitivities/' + str(r) + 'RxnSensitivity.csv')
                    else:
                        data = pd.read_csv('./linearscaling/' + file_location + '/sensitivities/' + str(r) + 'ThermoSensitivity.csv')
                placeholders = []
                for y in range(len(data.get_values())):
                    placeholders.append(data.get_values()[y][1])
                # generate fake placeholder data
                fakedata = np.zeros_like(placeholders, dtype=float)  # placeholder data is 0.0 (float)
#                 fakedata = np.full_like(placeholders, np.inf, dtype=float)  # placeholder data is inf
                return zip(placeholders, fakedata)
                break
            except:
                continue


array = os.listdir('./linearscaling/')
array = sorted(array)

allrxndata = []  # where all rxn sens itivities will be stored
allthermodata = []

ratios = [0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6]
for f in array:
    rxndata = []
    thermodata = []
    for ratio in ratios:
        # for reaction sensitivities
        rxndata.append([ratio, import_sensitivities(ratio, file_location=f)])
        allrxndata.append([rxndata])  # save each binding energy to where all data will live

        # for thermo sensitivities
        thermodata.append([ratio, import_sensitivities(ratio, file_location=f, thermo=True)])
        allthermodata.append([thermodata])

    # check to see an entire C/O ratio failed
    # might not need this check here, should be caught when the above can't load dict_conversions_selectivities
    for x in range(len(rxndata)):
        if rxndata[x][1] is None:
            print('CANNOT LOAD ANY RXN SENSITIVITIES FOR:    ' + f)
            break
        if thermodata[x][1] is None:
            print('CANNOT LOAD ANY THERMO SENSITIVITIES FOR: ' + f)
            break