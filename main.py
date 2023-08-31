#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
#                               MAIN PROGRAM
# =============================================================================

#%% Imports

import geopandas as gpd

# Import evolutionary algorithm
from evolutionary_algorithm import evolve

# Import additional functions for plotting
from plotting_functions import make_ser_and_vna_table, make_chart, \
    make_plot, make_county_boundary_plot, make_full_plot, make_double_chart

# Import additional functions for data analysis
from data_analysis import find_full_state, convert_data, remove_islands

#%% Files

# Read in data
d0 = gpd.read_feather('./data/IrishElectoralDivisions.feather')
# d0 = gpd.read_feather('./data/IrishElectoralDivisionsWithoutDublin.feather')
# Uncomment to use dataset with Dublin removed

# Convert data to appropriate types
d0 = convert_data(d0)

#%% Initialisation

# Make a copy of the dataframe
d = d0.copy()

# Remove Islands
d = remove_islands(d)

# Re-run this cell to re-initialise the data
    
#%% Parameters

flips = 5 # Number of ED flips per child state
kids = 10 # Number of child states per generation
keep = 4 # Number of child states to retain per generation
# Number of culls per generation = kids - keep

#%% Run

# Run the evolutionary algorithm to get three best states
optimal_states, optimal_rewards = evolve(d, flips, kids, keep)
optimal_state = optimal_states[0] # Get overall best state

#%% Full State

# Run find_full_state to add islands back into dataset (for plotting)
# Set add_dublin=True if Dublin was not included in the evolution
original_data_full = find_full_state(d0, add_dublin=False)
optimal_data_full = find_full_state(optimal_state, add_dublin=False)

#%% Full Numbered Plot

make_full_plot(original_data_full)

#%% Plots

make_plot(
    original_data_full, 
    'original_state'
    )

make_plot(
    optimal_data_full, 
    f'optimal_state_flips={flips}_kids={kids}_keep={keep}'
    )

#%% Plot with Changes Highlighted

make_plot(
    optimal_data_full, 
    f'optimal_state_flips={flips}_kids={kids}_keep={keep}',
    highlight_changes=True
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
make_chart(
    original_data_full, 
    optimal_data_full, 
    f'flips={flips}_kids={kids}_keep={keep}',
    save_tex=True
    )

#%% VNA Chart

# Bar chart comparing VNAs of original and optimal state
make_chart(
    original_data_full,
    optimal_data_full,
    f'flips={flips}_kids={kids}_keep={keep}',
    metric='VNA',
    save_tex=True
    )

#%% Double Chart Showing SER and VNA

make_double_chart(
    original_data_full, 
    optimal_data_full,
    save_tex=True
    )

#%% SER and VNA Tables

make_ser_and_vna_table(
    original_data_full, 
    'original_state'
    )
make_ser_and_vna_table(
    optimal_data_full, 
    f'optimal_state_SER_flips={flips}_kids={kids}_keep={keep}'
    )

#%% Save Data

# Probably only bother with this if the optimal state is really good
optimal_data_full.to_feather(
    f'./data/optimal_data_good_flips={flips}_kids={kids}_keep={keep}.feather')