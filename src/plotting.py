# contains functions to generate plots used in app.py

import pandas as pd
import numpy as np
import plotly.express as px
import os
import matplotlib
matplotlib.use('Agg')  # For non-GUI plotting (good for saving to files)
from whittaker_eilers import WhittakerSmoother
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from astropy.timeseries import LombScargle
import pyleoclim as pyleo

#####################################################################
# LR04
#####################################################################
# For plotting
# First 104 MIS boundaries according to LR04 - till 2614ka
mis_bounds = pd.read_csv('assets/LR04_MISboundaries.txt', skiprows=2, delimiter='\t\t', usecols=[1], header=None, engine='python')    #dtype={'a': str, 'b': np.float64}, 
mis_bounds = mis_bounds.iloc[:109,0].to_numpy()
mis_bounds = np.delete(mis_bounds, [2, 3, 4, 5, 6, 7, 8])
mis_bounds = mis_bounds[mis_bounds<=1500]
mis_bounds = np.insert(mis_bounds, 0, 0)

# For Tables
# First 104 MIS boundaries according to LR04 - till 2614ka
mis_bounds_temp = pd.read_csv('assets/LR04_MISboundaries.txt', skiprows=2, delimiter='\t\t', usecols=[1], header=None, engine='python')    #dtype={'a': str, 'b': np.float64}, 
mis_bounds_temp = mis_bounds_temp.iloc[:109,0].to_numpy() 

bounds = []
j=1
for i, bound in enumerate(mis_bounds_temp):
    if i==0:
        bounds.append([0,bound,str(j),(i+1)%2])
    elif j==4:
        j=j+1
        bounds.append([71.0,130.0,str(j),j%2])
    else:
        if np.isfinite(mis_bounds_temp[i-1]) and np.isfinite(bound):
            j=j+1
            bounds.append([mis_bounds_temp[i-1],bound,str(j),j%2])


#####################################################################
# Prob-stack
#####################################################################

# First 50 MIS boundaries according to Prob-stack (Tzedkais et al. 2017 method) - last 1.5 Ma
bounds_probstack = pd.read_csv('assets/Prob-stack_MISboundaries.csv').to_numpy()   

#####################################################################
# Prob-stack2 - only glacial terminations, no glacial onsets
#####################################################################

# First 50 MIS boundaries according to Prob-stack (Tzedkais et al. 2017 method) - last 1.5 Ma
bounds_probstack2 = pd.read_csv('assets/Prob-stack_MISboundaries-2.csv').to_numpy()   


# data must be in format:
# data = np.array([
#           [age_LR04, bd18O_LR04, True],
#           [age_probstack, bd18O_probstack, True], 
#        ], dtype=object)
def calc_extrema(data, mis_bounds):
    extrema = [ [] for _ in range(data.shape[0]) ]
    
    for d in range(data.shape[0]):
        for i, bound in enumerate(mis_bounds[:-1]):
            # IG
            if (i%2)==0:
                # print(f'MIS bounds: {mis_bounds[i]}-{mis_bounds[i+1]}')
                time_mask = np.where(np.logical_and(mis_bounds[i]<=data[d,0], 
                                                    data[d,0]<=mis_bounds[i+1]))[0]
                # print('INTERGLACIAL\n',age_data[d][time_mask])
    
                # check if data within MIS and if only NaN
                if len(time_mask)>0 and np.any(np.isfinite(data[d,1][time_mask])):
                    if data[d,2]:
                        id_IG = np.nanargmin(data[d,1][time_mask])
                    else:
                        id_IG = np.nanargmax(data[d,1][time_mask])
                    
                    # print(f'i+1={i+1}; Bounds={mis_bounds[i]}-{mis_bounds[i+1]}')
                    # print(f'id_IG={id_IG}')
                    # print(f'time={data[d,0][time_mask[id_IG]]}, Min={data[d,1][time_mask][id_IG]}\n')
                    extrema[d].append([data[d,0][time_mask[id_IG]], data[d,1][time_mask][id_IG], 1])
                else:
                    # MIS not included/Only NaN
                    extrema[d].append([np.nan, np.nan, 1])
                
            else:
                # print(f'MIS bounds: {mis_bounds[i]}-{mis_bounds[i+1]}')
                time_mask = np.where(np.logical_and(mis_bounds[i]<=data[d,0], 
                                                    data[d,0]<=mis_bounds[i+1]))[0]
                # print('GLACIAL\n',data[d,0][time_mask])
    
                # check if data within MIS and if only NaN
                if len(time_mask>0) and np.any(np.isfinite(data[d,1][time_mask])):
                    if data[d,2]:
                        id_G = np.nanargmax(data[d,1][time_mask])
                    else:
                        id_G = np.nanargmin(data[d,1][time_mask])
                    
                    # print(f'i+1={i+1}; Bounds={mis_bounds[i]}-{mis_bounds[i+1]}')
                    # print(f'id_G={id_G}')
                    # print(f'time={data[d,0][time_mask[id_G]]}, Max={data[d,1][time_mask][id_G]}\n')    
                    extrema[d].append([data[d,0][time_mask[id_G]], data[d,1][time_mask][id_G], 0])
                else:
                    # MIS not included/Only NaN
                    extrema[d].append([np.nan, np.nan, 0])
    
    extrema = np.array(extrema)
    print(extrema.shape)
    return extrema


# Used for bounds_probstack2 (only glacial terminations)
# data must be in format:
# data = np.array([
#           [age_LR04, bd18O_LR04, True],
#           [age_probstack, bd18O_probstack, True], 
#        ], dtype=object)
def calc_extrema_only_terminations(data, mis_bounds):
    extrema = [ [] for _ in range(data.shape[0]) ]
    
    for d in range(data.shape[0]):
        for i, (start, end, mis, state) in enumerate(mis_bounds):
            # IG
            if state==1:
                # print(f'MIS bounds: {mis_bounds[i]}-{mis_bounds[i+1]}')
                time_mask = np.where(np.logical_and(start<=data[d,0], 
                                                    data[d,0]<=end))[0]
                # print('INTERGLACIAL\n',age_data[d][time_mask])
    
                # check if data within MIS and if only NaN
                if len(time_mask)>0 and np.any(np.isfinite(data[d,1][time_mask])):
                    if data[d,2]:
                        id_IG = np.nanargmin(data[d,1][time_mask])
                    else:
                        id_IG = np.nanargmax(data[d,1][time_mask])
                    
                    # print(f'i+1={i+1}; Bounds={mis_bounds[i]}-{mis_bounds[i+1]}')
                    # print(f'id_IG={id_IG}')
                    # print(f'time={data[d,0][time_mask[id_IG]]}, Min={data[d,1][time_mask][id_IG]}\n')
                    extrema[d].append([data[d,0][time_mask[id_IG]], data[d,1][time_mask][id_IG], 1])
                else:
                    # MIS not included/Only NaN
                    extrema[d].append([np.nan, np.nan, 1])
                
            else:
                # print(f'MIS bounds: {mis_bounds[i]}-{mis_bounds[i+1]}')
                time_mask = np.where(np.logical_and(start<=data[d,0], 
                                                    data[d,0]<=end))[0]
                # print('GLACIAL\n',data[d,0][time_mask])
    
                # check if data within MIS and if only NaN
                if len(time_mask>0) and np.any(np.isfinite(data[d,1][time_mask])):
                    if data[d,2]:
                        id_G = np.nanargmax(data[d,1][time_mask])
                    else:
                        id_G = np.nanargmin(data[d,1][time_mask])
                    
                    # print(f'i+1={i+1}; Bounds={mis_bounds[i]}-{mis_bounds[i+1]}')
                    # print(f'id_G={id_G}')
                    # print(f'time={data[d,0][time_mask[id_G]]}, Max={data[d,1][time_mask][id_G]}\n')    
                    extrema[d].append([data[d,0][time_mask[id_G]], data[d,1][time_mask][id_G], 0])
                else:
                    # MIS not included/Only NaN
                    extrema[d].append([np.nan, np.nan, 0])
    
    extrema = np.array(extrema)
    return extrema
    
# Define custom colormaps
white_to_red = mcolors.LinearSegmentedColormap.from_list("white_to_red", ["white", "#c00000"])
white_to_red_r = white_to_red.reversed()
white_to_blue = mcolors.LinearSegmentedColormap.from_list("white_to_blue", ["white", "#002060"])
white_to_blue_r = white_to_blue.reversed()
white_to_purple = mcolors.LinearSegmentedColormap.from_list("white_to_purple", ["white", "#7030a0"])
white_to_purple_r = white_to_purple.reversed()

# Register the colormaps
matplotlib.colormaps.register(name='white_to_red', cmap=white_to_red, force=True)
matplotlib.colormaps.register(name='white_to_red_r', cmap=white_to_red_r, force=True)
matplotlib.colormaps.register(name='white_to_blue', cmap=white_to_blue, force=True)
matplotlib.colormaps.register(name='white_to_blue_r', cmap=white_to_blue_r, force=True)
matplotlib.colormaps.register(name='white_to_purple', cmap=white_to_purple, force=True)
matplotlib.colormaps.register(name='white_to_purple_r', cmap=white_to_purple_r, force=True)

# Creates pd.DataFrames for the IG and G strengths
def create_dfs(df, selected_metric, extrema, y_invert, bounds):
    # Index for DataFrame
    df_index = df.loc[0, (selected_metric, 'variable')]
    
    ########################################################################
    ###         Split extrema list for IGs and Gs
    nrows = np.shape(extrema)[0]

    extremas_IG = []
    extremas_G = []
    for row in range(nrows):
        # get IG/G extrema from all extrema
        extrema_IG = np.where(extrema[row][:,2]==1)[0]
        extrema_IG = extrema[row][extrema_IG,:2]
        
        extrema_G = np.where(extrema[row][:,2]==0)[0]
        extrema_G = extrema[row][extrema_G,:2]

        extremas_IG.append(extrema_IG)
        extremas_G.append(extrema_G)

    ########################################################################
    ###             IG
             
    # Column names for IG strength table    
    if bounds=='LR04':
        # for LR04
        columns_IG = ['MIS ' + str(i) for i in range(5,50,2)]
        columns_IG = np.insert(columns_IG, 0, 'MIS 1')
    elif bounds=='Prob-stack' or bounds=='Prob-stack2':
        columns_IG = ['MIS ' + s for s in bounds_probstack[::2, 2]]

    data_IG = []
    for row in range(np.shape(extrema)[0]):
        data_IG.append(extremas_IG[row][:,1])

    df_IG = pd.DataFrame(data_IG, columns=columns_IG)
    df_IG.index = [df_index]

    if y_invert:
        df_IG = df_IG.style.background_gradient(cmap='white_to_red_r', axis=1).format("{:.2f}")
    else:
        df_IG = df_IG.style.background_gradient(cmap='white_to_red', axis=1).format("{:.2f}")
    
    ########################################################################
    ###             G

    # Column names for G strength table   
    if bounds=='LR04':
        # for LR04
        columns_G = ['MIS ' + str(i) for i in range(6,50,2)]
        columns_G = np.insert(columns_G, 0, 'MIS 2')
    elif bounds=='Prob-stack' or bounds=='Prob-stack2':
        columns_G = ['MIS ' + s for s in bounds_probstack[1::2, 2]]

    data_G = []
    for row in range(np.shape(extrema)[0]):
        data_G.append(extremas_G[row][:,1])

    df_G = pd.DataFrame(data_G, columns=columns_G)
    df_G.index = [df_index]

    if y_invert:
        df_G = df_G.style.background_gradient(cmap='white_to_blue', axis=1).format("{:.2f}")
    else:
        df_G = df_G.style.background_gradient(cmap='white_to_blue_r', axis=1).format("{:.2f}")

    ########################################################################
    ###             Amplitudes

    if bounds=='LR04':
        # for LR04
        columns_amplitude = ['MIS ' + str(i) + '/' + str(i+1) for i in range(7,49,2)]
        columns_amplitude = np.insert(columns_amplitude, 0, 'MIS 1/2')
        columns_amplitude = np.insert(columns_amplitude, 1, 'MIS 5/6')
    elif bounds=='Prob-stack' or bounds=='Prob-stack2':
        # for probstack
        columns_amplitude = np.array([f'MIS {bounds_probstack[:,2][2*i]}/{bounds_probstack[:,2][2*i+1]}' for i in range(len(bounds_probstack[::2,2]) - 1)])


    data_amplitude = np.absolute(np.array(data_IG)[:,:-1] - np.array(data_G))
    df_amplitude = pd.DataFrame(data_amplitude, columns=columns_amplitude)
    df_amplitude.index = [df_index]

    df_amplitude = df_amplitude.style.background_gradient(cmap='white_to_purple', axis=1).format("{:.2f}")

    return df_IG, df_G, df_amplitude

# Calculates Lomb-Scargle Periodograms
def calc_lombscargle(age, data):
    # Spectral analysis: Periodogram
    # Split into 2 diagrams: before 800 kyr, 1Ma-1.5Ma

    age_postMPT = age[age<=800]
    age_preMPT = age[np.logical_and(1000<=age, age<=1500)]
    data_postMPT = data[age<=800]
    data_preMPT = data[np.logical_and(1000<=age, age<=1500)]

    # check for nans in arrays
    age_data_pairs = [
        [age_preMPT, data_preMPT],
        [age_postMPT, data_postMPT],
    ]

    for i, (age, data) in enumerate(age_data_pairs):
        mask = np.isfinite(age) & np.isfinite(data)
        age_data_pairs[i][0] = age[mask]
        age_data_pairs[i][1] = data[mask]

    # Unpack the cleaned data
    age_preMPT, data_preMPT = age_data_pairs[0]
    age_postMPT, data_postMPT = age_data_pairs[1]

    f_LombScargle_postMPT, P_LombScargle_postMPT = LombScargle(age_postMPT, data_postMPT, normalization='standard').autopower(minimum_frequency=1/150, maximum_frequency=1/10)
    f_LombScargle_preMPT, P_LombScargle_preMPT = LombScargle(age_preMPT, data_preMPT, normalization='standard').autopower(minimum_frequency=1/150, maximum_frequency=1/10)
    
    return [(f_LombScargle_postMPT, P_LombScargle_postMPT), (f_LombScargle_preMPT, P_LombScargle_preMPT)]

# Create a summary plot in pyeloclim: Scalogram and spectral plot
def pyleo_plot(age, data, y_invert, name, label):
    ts = pyleo.Series(time=age,
                    value= data,
                    time_name='Age',time_unit='ka',
                    value_name=name,
                    label=name, verbose=False).interp(step=1)

    psd = ts.spectral()
    scal = ts.wavelet(freq_kwargs={'fmin':1/500,'fmax':1/5,'nf':50})
    scal_sig = scal.signif_test(method='ar1asym')

    fig, ax = ts.summary_plot(psd.beta_est(), scal_sig, figsize=(12,8), title=label)
    if y_invert:
        ax['ts'].invert_yaxis()
    ax['scal'].vlines(0, 5, 500, colors='grey', linestyles='--', linewidth=3)
    ax['scal'].hlines(y=[23, 41, 100], xmin=np.nanmin(0), xmax=np.nanmax(age), colors='red', linestyles='--', label='Orbital frequencies')
    # fig, ax = scal_sig.plot(figsize=(12,8))

    rand_id = str(np.random.randint(low=1e5, high=9e5))
    file_path = f'assets/pyleo_plot-{rand_id}.png'
    if os.path.exists(file_path):
         os.remove(file_path)
    pyleo.utils.plotting.savefig(fig, path=file_path, dpi=300)

    return file_path
    

# Apply Whittaker-Eilers smoothing with order 3 and optimal lambda
def smoothing(age, data, lam, output=False):
    # only use non-nan values
    # if nans occure in interval 0:len, doesn't matter, since deleted from age and data
    # Note, array is filled with nans, after len
    ids = ~np.isnan(data)
    age_nonnan = age[ids]
    data_nonnan = data[ids]

    if lam == None:
        # Apply Whittaker-Eilers smoothing
        whittaker_smoother = WhittakerSmoother(
            lmbda=2e4, order=3, data_length=len(data_nonnan)
        )
        optimal_smooth = whittaker_smoother.smooth_optimal(data_nonnan)
        print("Optimal lambda: {}".format(optimal_smooth.get_optimal().get_lambda()))
        optimal_data_smooth = optimal_smooth.get_optimal().get_smoothed()

        l = optimal_smooth.get_optimal().get_lambda()

    else:
        # Apply Whittaker-Eilers smoothing
        whittaker_smoother = WhittakerSmoother(
            lmbda=lam, order=3, data_length=len(data_nonnan)
        )
        optimal_data_smooth = whittaker_smoother.smooth(data_nonnan)

        l = lam

    n = len(data) - len(data_nonnan)
    optimal_data_smooth.extend([np.nan]*n)
    age_nonnan = np.append(age_nonnan, [np.nan]*n)

    if output:
        return l

    return age_nonnan, np.array(optimal_data_smooth)

