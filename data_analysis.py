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

#%% Files

dublin = gpd.read_feather('./data/DublinElectoralDivisions.feather')
islands = gpd.read_feather('./data/IslandElectoralDivisions.feather')
counties = gpd.read_feather('./data/IrishCounties.feather')

#%% Convert Data Types

def convert_data(df):
    '''
    Converts data arrays to appropriate types.
    '''
    for i in range(len(df)):
        df.at[i,'NEIGHBOURS'] = df.at[i,'NEIGHBOURS'].astype(int)
        df.at[i,'NB_CONS'] = df.at[i,'NB_CONS'].astype(str)
    return df

#%%
dublin = convert_data(dublin)

#%% Get Indices
  
def get_indices(ed_ids, df):
    '''
    Takes in an array of ED IDs and returns an array 
    of corresponding row indices.
    '''
    indices = []
    for n in ed_ids:
        if list(df.loc[df['ED_ID']==n].index) != []:
            indices.append(list(df.loc[df['ED_ID']==n].index)[0])
    return np.array(indices)

#%% Find Neighbours

def find_neighbours(df):
    '''
    Finds the neighbours and neighbouring CONs of each ED in the dataframe.
    '''
    # Create column containing empty neigbours list for each ED
    df['NEIGHBOURS'] = [[] for i in  range(len(df))]
    df['NB_CONS'] = [[] for i in  range(len(df))]
    df['BOUNDARY'] = [1 for i in  range(len(df))]
    df['CHANGE'] = [0 for i in  range(len(df))]
    
    # Find neighbours of each ED
    for i in range(len(df)):
        t = df['geometry'][i].touches(df['geometry'].values)
        # Create column of neighbouring EDs
        df.at[i,'NEIGHBOURS'] = df['ED_ID'][t].tolist()
        # Create column of neighbouring CONs        
        df.at[i,'NB_CONS'] = list(np.unique((df.loc[t,'CON']).tolist()))
        # Remove self from column
        if df.at[i,'CON'] in df.at[i,'NB_CONS']:
            df.at[i,'NB_CONS'].remove(df.at[i,'CON'])
        # Set type of ED
        if df.at[i,'NB_CONS'] == []:
            # No neighbouring CONs -> interior
            df.at[i,'BOUNDARY'] = 0
        df.at[i,'NEIGHBOURS'] = np.array(df.at[i,'NEIGHBOURS']).astype(str)
        df.at[i,'NB_CONS'] = np.array(df.at[i,'NB_CONS']).astype(str)
    
    return df

#%% Remove Islands

def remove_islands(df):
    '''
    Removes eight wholly-island EDs from dataframe. 
    Required for contiguity check to function properly.
    '''
    try:
        # Get indices to be removed
        to_remove = [df[df['ED'] == ed].index.item() 
                     for ed in list(islands['ED'])]
        # Remove all eight wholly-island EDs
        df2 = df.drop(to_remove).reset_index(drop=True)
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
    df2 = df.drop(to_remove).reset_index(drop=True)
    return df2

#%% Find Full State

def find_full_state(df, add_dublin=False):
    '''
    Replaces eight wholly-island EDs in dataframe.
    If add_dublin=True, then also replaces EDs in Dublin.
    '''
    if add_dublin:
        df2 = gpd.GeoDataFrame(pd.concat([df, dublin, islands]))
    else:
        df2 =  gpd.GeoDataFrame(pd.concat([df, islands]))
    df2 = df2.reset_index(drop=True)
    df2['CON'] = df2['CON'].str.upper()
    return df2

#%% SER

def ser(df, c, national_ratio=29800):
    '''
    Returns SER (Seat Equivalent Representation) of constituency c.
    '''
    data = df[df['CON']==c]
    pop = data['POPULATION'].sum()
    return pop/national_ratio

#%% VNA

def vna(df, c, use_current_seats=False, national_ratio=29800):
    '''
    Returns VNA (Variance from National Average) of constituency c.
    '''
    ser_val = ser(df, c)
    if use_current_seats:
        seats = int(df[df['CON']==c].reset_index(drop=True)['SEATS'][0])
        return (ser_val - seats)/seats
    return (ser_val - round(ser_val))/round(ser_val)

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

#%% VNA Global

def vna_global(df, use_current_seats=False, national_ratio=29800):
    '''
    Returns dictionary containing VNA values for each constituency.
    '''
    vna_dict = {}
    df['CON'] = df['CON'].str.upper()
    for c in np.unique(df['CON'].to_list()):
        s = vna(df, c, use_current_seats, national_ratio)
        vna_dict[c] = s
    return vna_dict
