#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 11:10:27 2023

@author: elizasomerville
"""

# =============================================================================
#                               MAIN PROGRAM
# =============================================================================

#%% Imports

#import numpy as np
import geopandas as gpd

# Import evolutionary algorithm
from evolutionary_algorithm import evolve

# Import additional functions for plotting
from plotting_functions import make_ser_table, make_ser_chart, \
    make_plot, make_county_boundary_plot

# Import additional functions for data analysis
from data_analysis import find_full_state, convert_data, remove_islands, \
    remove_dublin

#%% Files

# Read in data
d0 = gpd.read_feather('./data/ed_and_ct_data.feather')

# Convert data to appropriate types
d0 = convert_data(d0)

#%% Copy

# Make a copy of the dataframe
d = d0.copy()
# Re-run this cell to re-initialise the data

#%% Remove Islands

d = remove_islands(d)

#%% Remove Dublin

# Remove Dublin from the dataset, if desired
d_no_dub = remove_dublin(d)
    
#%% Parameters

flips = 5 # Number of ED flips per configuration
kids = 10 # Number of child states per generation
keep = 3 # Number of child states to retain per generation

#%% Run

# Run the evolutionary algorithm
optimal_state, optimal_reward = evolve(d, flips, kids, keep)

#%% Full State

# Run find_full_state to add islands back into dataset (for plotting)
# Set add_dublin=True if Dublin was not included in the evolution
original_data_full = find_full_state(d, add_dublin=False)
optimal_data_full = find_full_state(optimal_state, add_dublin=False)

#%% Plots

make_plot(
    original_data_full, 
    'original_state'
    )
make_plot(
    optimal_data_full, 
    f'optimal_state_flips={flips}_kids={kids}_keep={keep}'
    )

#%% County Boundary Plots

# Same as before, except also overlaid with county boundaries
make_county_boundary_plot(
    original_data_full, 
    'original_state'
    )
make_county_boundary_plot(
    optimal_data_full, 
    f'optimal_state_flips={flips}_kids={kids}_keep={keep}'
    )

#%% SER Chart

# Bar chart comparing SERs of original and optimal state
make_ser_chart(
    original_data_full, 
    optimal_data_full, 
    f'SER_w_dub_{flips}_{kids}_{keep}'
    )

#%% SER Tables

make_ser_table(
    original_data_full, 
    'original_state'
    )
make_ser_table(
    optimal_data_full, 
    f'optimal_state_SER_{flips}_{kids}_{keep}'
    )

#%% Save Data

# Probably only bother with this if the optimal state is really good
optimal_data_full.to_feather(f'./data/optimal_data_w_dub_7_{flips}_{kids}_{keep}.feather')