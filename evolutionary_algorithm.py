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
#   2. Respect of county boundaries
#   3. Continuity over time
#   4. Compactness (convex hull) (not currently implemented)
from reward_function import reward

# =============================================================================
#                           FUNCTION DEFINITIONS
# =============================================================================
  
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

#%% Flip

def flip(df_orig):
    '''
    Randomly swaps the CT of a boundary ED.
    '''
    # Make copy of input dataframe
    df = df_orig.copy()
    
    # Filter the dataframe to contain only boundary EDs 
    # which have not previously changed
    data = df[(df['BOUNDARY']!=0)&(df['CHANGE']<1)].copy()
    
    # Randomly choose one of the filtered EDs
    i = int(random.choice(data.index.to_list()))
    # Get pre-flip CT of chosen ED
    old_con = df.at[i,'CON']
    # Choose random neighbouring CT of chosen ED
    new_con = random.choice(df.at[i,'NBH_CONS'])
    # Update the CT of of the chosen ED; this is the 'flip'
    df.at[i,'CON'] = new_con
    # Update CHANGE to record that this ED has changed
    if df.at[i,'CHANGE'] == 1:
        df.at[i,'CHANGE'] = 2
    else:
        df.at[i,'CHANGE'] = 1
    # Ensure no ED has its own CT as a neighbour
    i0 = np.where(df.at[i,'NBH_CONS']==new_con)
    df.at[i,'NBH_CONS'] = np.delete(df.at[i,'NBH_CONS'],i0)
    
    # Get an array of indices of neighbouring EDs
    nbh_ed_ids = df.at[i,'NEIGHBOURS']
    nbh_indices = []
    for n in nbh_ed_ids:
        nbh_indices.append(df.loc[df['ED_ID']==n].index[0])
        
    # For each neighbouring ED y, if new_con is not listed in its neighbouring
    # CTs, then append it to the list
    for y in nbh_indices:
        if new_con not in list(df.at[y,'NBH_CONS']):
            df.at[y,'NBH_CONS'] = np.append(df.at[y,'NBH_CONS'], new_con)
            
        # Neighbouring EDs of y
        nbh_ed_ids_y = df.at[y,'NEIGHBOURS']
        nbh_indices_y = []
        for n2 in nbh_ed_ids_y:
            nbh_indices_y.append(df[df['ED_ID']==n2].index[0])
            
        # Count number of neighbours of y which are in old_con
        count = 0
        for z in nbh_indices_y:
            if df.at[z,'CON'] == old_con:
                count += 1
        # If no neighbours of y in old_con, remove old_con from the list of
        # neighbouring CTs of y
        if count == 0:
            i1 = np.where(df.at[y,'NBH_CONS']==old_con)
            df.at[y,'NBH_CONS'] = np.delete(df.at[y, 'NBH_CONS'], i1)
            # If y has no neighbouring CTs, then it is
            # not a boundary ED
            #if df.at[y,'NBH_CONS'].size == 0:
                #df.at[y,'BOUNDARY'] = 0
                
    for j in range(len(df)):
        if df.at[j,'NBH_CONS'].size == 0:
            df.at[j,'BOUNDARY'] = 0
# =============================================================================
#         if df.at[y,'BOUNDARY'] == 0:
#             df.at[y,'BOUNDARY'] = 2
# =============================================================================
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
    optimal_state = final_states[0]
    optimal_reward = final_rewards[0]
    
    return optimal_state, optimal_reward