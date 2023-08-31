#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 27 09:35:30 2023

@author: elizasomerville
"""
# =============================================================================
#                          EVOLUTIONARY ALGORITHM
# =============================================================================

#%% Imports

import numpy as np
import random

# Import reward function, which will first get rid of any non-contiguous 
# solutions, and then rank a particular state according to:
#   1. SER
#   2. Respect for county boundaries
#   3. Continuity over time
#   4. Compactness (convex hull) (not currently implemented)
from reward_function import reward

# =============================================================================
#                           FUNCTION DEFINITIONS
# =============================================================================

#%% Flip

def flip(df_orig):
    '''
    Randomly swaps the CON of a boundary ED.
    '''
    # Make copy of input dataframe
    df = df_orig.copy()
    
    # Filter the dataframe to contain only boundary EDs 
    # which have not previously changed, and have non-zero population
    pool = df[(df['BOUNDARY']!=0)&(df['CHANGE']<1)&(df['POPULATION']>0)]
    
    # Randomly choose one of the filtered EDs
    i = int(random.choice(pool.index.to_list()))
    # Get pre-flip CON of chosen ED
    old_con = df.at[i,'CON']
    # Choose random neighbouring CON of chosen ED
    new_con = random.choice(df.at[i,'NB_CONS'])
    # Update the CON of of the chosen ED; this is the 'flip'
    df.at[i,'CON'] = new_con
    # Update CHANGE to record that this ED has changed
    if df.at[i,'CHANGE'] == 1:
        df.at[i,'CHANGE'] = 2
    else:
        df.at[i,'CHANGE'] = 1
    # Ensure no ED has its own CON as a neighbour
    i0 = np.where(df.at[i,'NB_CONS']==new_con)
    df.at[i,'NB_CONS'] = np.delete(df.at[i,'NB_CONS'],i0)
    
    # Get an array of indices of neighbouring EDs
    nb_ed_ids = df.at[i,'NEIGHBOURS']
    nb_indices = []
    for n in nb_ed_ids:
        nb_indices.append(df.loc[df['ED_ID']==n].index[0])
        
    # For each neighbouring ED y, if new_con is not listed in its neighbouring
    # CONs, then append it to the list
    for y in nb_indices:
        if new_con not in list(df.at[y,'NB_CONS']):
            df.at[y,'NB_CONS'] = np.append(df.at[y,'NB_CONS'], new_con)
            
        # Neighbouring EDs of y
        nb_ed_ids_y = df.at[y,'NEIGHBOURS']
        nb_indices_y = []
        for n2 in nb_ed_ids_y:
            nb_indices_y.append(df[df['ED_ID']==n2].index[0])
            
        # Count number of neighbours of y which are in old_con
        count = 0
        for z in nb_indices_y:
            if df.at[z,'CON'] == old_con:
                count += 1
        # If no neighbours of y in old_con, remove old_con from the list of
        # neighbouring CONs of y
        if count == 0:
            i1 = np.where(df.at[y,'NB_CONS']==old_con)
            df.at[y,'NB_CONS'] = np.delete(df.at[y, 'NB_CONS'], i1)

    # If an ED has no neighbouting EDs, then it is not a boundary ED
    for j in range(len(df)):
        if df.at[j,'NB_CONS'].size == 0:
            df.at[j,'BOUNDARY'] = 0
        else:
            df.at[j,'BOUNDARY'] = 1

    return df

#%% Sort Array

def sort_array(arr):
    '''
    Sorts an array according to its second index.
    '''
    arr = sorted(arr, key=lambda x : x[1], reverse=True)
    return arr

#%% Reproduce

# Take an argument df corresponding to the parent of the generation
def reproduce(df, flips=10, kids=10):
    '''
    Takes in a parent dataframe df and outputs a list containing <kid> child 
    dataframes on which <flips> random flips have been performed.
    '''
    offspring = []
    for j in range(kids):
        kid_data = df.copy()
        for i in range(flips):
            kid_data = flip(kid_data)
        offspring.append(kid_data)
    return offspring

#%% Kill

def kill(offspring, keep=10):
    '''
    Takes in a list of child dataframes, computes the reward function for each, 
    and outputs a list with entries [child dataframe, corresponding reward]
    for the <keep> best children.
    '''
    chopping_block=[]
    for x in offspring:
        kid_data = x.copy()
        # Compute rewards
        r = reward(kid_data)
        chopping_block.append([x,r])
    # Sort by rewards and retain dataframes with <keep> highest rewards
    the_chosen_ones = sort_array(chopping_block)[:keep]
    return the_chosen_ones

#%% Compare

def compare(survivor, global_best, keep=10):
    '''
    Takes in a [df, reward] pair for a surviving child dataframe,
    and compares the reward to the global best from previous generations.
    Outputs a list of the <keep> best states and rewards.
    '''
    # If reward r is better than max of global_best, then replace min of
    # global_best with [state, r]
    if survivor[1] > global_best[0][1]:
        global_best[-1] = survivor
    # Return <keep> best survivors
    return sort_array(global_best)[:keep]

#%% Evolve
def evolve(df_orig, flips=10, kids=25, keep=3):
    '''
    Evolve original state to find improved state.
    '''
    df = df_orig.copy()
    # Create parents
    parents_and_rewards = kill(reproduce(df, flips, kids), keep)
    # Initialise global_best
    global_best = sort_array(parents_and_rewards)

    # Main evolutionary loop
    i = 1
    for parent_and_reward in parents_and_rewards:
        # Get parent df
        parent = parent_and_reward[0]
        # Find children
        children_and_rewards = kill(reproduce(parent, flips, kids), keep)
        j = 1
        for child_and_reward in children_and_rewards:
            # Update global_best
            global_best = compare(child_and_reward, global_best, keep)
            # Get child df
            child = child_and_reward[0]
            # Print status update
            print(f'Parent {i}, Child {j}')
            # Find grandchildren
            gchildren_and_rewards = kill(reproduce(child, flips, kids), keep)
            k = 1
            for gchild_and_reward in gchildren_and_rewards:
                k += 1
                # Update global_best
                global_best = compare(gchild_and_reward, global_best, keep)
            j += 1
        i += 1
                
    final_states = list(map(list, zip(*global_best)))[0]
    final_rewards = list(map(list, zip(*global_best)))[1]
    
    # Return three best states and corresponding rewards
    return final_states[0:3], final_rewards[0:3]
