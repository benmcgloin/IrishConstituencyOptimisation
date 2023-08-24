#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 11:23:21 2023

@author: elizasomerville
"""

#%% Imports

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from reward_function import ser

plt.rcParams['figure.dpi'] = 300

#%% Files

dublin = gpd.read_feather('./data/dub.feather')
islands = gpd.read_feather('./data/islands.feather')
counties = gpd.read_feather('./data/county_data.feather')

#%% Convert Data Types

def convert_data(df):
    '''
    Converts data arrays to appropriate types.
    '''
    for i in range(len(df)):
        df.at[i,'NEIGHBOURS'] = df.at[i,'NEIGHBOURS'].astype(int)
        df.at[i,'NBH_CONS'] = df.at[i,'NBH_CONS'].astype(str)
    return df

#%%
dublin = convert_data(dublin)

#%% Find Neighbours

def find_neighbours(df):
    '''
    Finds the neighbours and neighbouring CTs of each ED in the dataframe.
    '''
    # Create column containing empty neigbours list for each ED
    df['NEIGHBOURS'] = [[] for i in  range(len(df))]
    df['NBH_CONS'] = [[] for i in  range(len(df))]
    df['BOUNDARY'] = [1 for i in  range(len(df))]
    df['CHANGE'] = [0 for i in  range(len(df))]
    
    # Find neighbours of each ED
    for i in range(len(df)):
        t = df['geometry'][i].touches(df['geometry'].values)
        # Create column of neighbouring EDs
        df.at[i,'NEIGHBOURS'] = df['ED_ID'][t].tolist()
        # Create column of neighbouring CTs        
        df.at[i,'NBH_CONS'] = list(np.unique((df.loc[t,'CON']).tolist()))
        # Remove self from column
        if df.at[i,'CON'] in df.at[i,'NBH_CONS']:
            df.at[i,'NBH_CONS'].remove(df.at[i,'CON'])
        # Set type of ED
        if df.at[i,'NBH_CONS'] == []:
            # No neighbouring CTs -> interior
            df.at[i,'BOUNDARY'] = 0
        df.at[i, 'NEIGHBOURS'] = np.array(df.at[i, 'NEIGHBOURS']).astype(str)
        df.at[i, 'NBH_CONS'] = np.array(df.at[i, 'NBH_CONS']).astype(str)
    
    return df

#%% Remove Islands

def remove_islands(df):
    '''
    Removes eight wholly-island EDs from dataframe. 
    Required for contiguity check to function properly.
    '''
    try:
        # Get indices to be removed
        to_remove = [df[df['ED'] == ed].index.item() for ed in list(islands['ED'])]
        # Remove all eight wholly-island EDs
        df2 = df.drop(to_remove)
        df2 = df2.reset_index(drop=True)
        return df2
    except ValueError:
        # This error occurs if the islands are not found in the dataframe
        print('No islands found to be removed.\nReturning original dataframe.')
        return df

#%% Remove Dublin

def remove_dublin(df):
    '''
    Removes all EDs in County Dublin from dataframe. 
    This may be desirable as Dublin EDs are very small and flips here
    may not have a significant effect on the overall configuration.
    '''
    # Get indices to be removed
    to_remove = list(df[df['COUNTY']=='DUBLIN'].index)
    # Remove all Dublin EDs
    df2 = df.drop(to_remove)
    df2 = df2.reset_index(drop=True)
    return df2

#%% Find Full State

def find_full_state(df, add_dublin=True):
    '''
    Replaces eight wholly-island EDs in dataframe.
    If add_dublin=True, then also replaces EDs in Dublin.
    '''
    if add_dublin:
        df2 = gpd.GeoDataFrame(pd.concat([df, dublin, islands]))
    else:
        df2 =  gpd.GeoDataFrame(pd.concat([df, islands]))
    df2 = df2.reset_index(drop=True)
    return df2

#%% SER Global

def ser_global(df, national_ratio=29800):
    '''
    Returns dictionary containing SER values for each constituency.
    '''
    ser_dict = {}
    df['CON'] = df['CON'].str.upper()
    for c in np.unique(df['CON'].to_list()):
        s = ser(df, c, national_ratio)
        ser_dict[c] = s
    return ser_dict