#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#%% Imports
import pandas as pd
import numpy as np
import networkx as nx # For contiguity check
from numba import jit # Use numba for faster computation

from data_analysis import ser

#%% Files

c2c = pd.read_csv('./data/ConstituencyCountyLink.csv')

#%% Constituency

def constituency(df, c):
    '''
    Finds union of all EDs in a constituency.
    '''
    data = df[df['CON']==c] # All EDs in given CON
    union = data.unary_union # Union of all EDs in given CON
    return union

#-------------------------------- CONTIGUITY ----------------------------------
        
#%% Contiguity

def f_contiguity(df):
    '''
    Checks whether all constituencies in the state are contiguous.
    Returns 1 if so, 0 if not.
    '''
    # Only check for changed constituenciess
    changed_cons = list(np.unique(df[df['CHANGE']==1]['CON']))
    # Neighbouring CONs of a flipped ED could also become discontiguous,
    # so add them to changed_cons
    for i in list(df[df['CHANGE']>0].index):
        for nc in df.loc[i, 'NB_CONS']:
            if nc not in changed_cons:
                changed_cons.append(nc)
    # Check contiguity of each changed constituency
    for c in changed_cons:
        # Filter dataframe to just EDs in constituency c
        d = df[df['CON']==c]
        # Create list of ED IDs in constituency c
        ed_ids = list(d['ED_ID'])
        # Form nested list of neighbours of each ED
        nbh_list = list([list(nbh) for nbh in d['NEIGHBOURS']])
        # Form nested list with only neighbours in constituency c
        nbhs_in_c = [[n for n in nbh_sublist if n in ed_ids] 
                for nbh_sublist in nbh_list]
        if [] in nbhs_in_c: # If some ED in CON c has no neighbours in same CON
            return 0
        # Create a dictionary of ED ID-neighbour pairs,
        # but only including neighbours in same constituency
        nbh_dict = {ed_id: nbh for ed_id, nbh in
                    zip(list(d['ED_ID']), nbhs_in_c)}
        # Create a graph representing constituency c
        g = nx.Graph(nbh_dict)
        # Check whether the graph is connected, i.e. whether c is contiguous
        if not nx.is_connected(g):
            return 0
    return 1
    
#-------------------------------- COMPACTNESS ---------------------------------
# Not currently implemented

#%% Polsby-Popper

def pp(geom):
    '''
    Checks compactness of a geometry using the Polsby-Popper test.
    '''
    p = geom.length
    a = geom.area
    return (4*np.pi*a)/(p**2)

#%% Schwartzberg

def schwartz(geom):
    '''
    Checks compactness of a geometry using the Schwartzberg test.
    '''
    p = geom.length
    a = geom.area
    return (2*np.pi*np.sqrt(a/np.pi))/p

#%% Convex Hull

def convex_hull(geom):
    '''
    Checks compactness of a geometry using the convex hull test.
    '''
    ch = geom.convex_hull
    return geom.area/ch.area

#%% Compactness

def f_compactness(df, a=0.3):
    '''
    Checks compactness of all constituencies.
    '''
    total = 0
    for c in np.unique(df['CON']):
        union = constituency(df, c)
        total += convex_hull(union)
    return a*total

#%% Exponential

@jit(nopython=True)
def f_exp(x, y, a, b):
    '''
    Exponential decay function.
    '''
    return np.exp(-a*x-b*y)

#------------------------------ COUNTY BOUNDARIES -----------------------------

#%% County Boundaries

def f_county_boundary(df, c2c=c2c, a=1e-10, b=1e-4):
    '''
    Checks how much state preserves county boundaries.
    '''
    num_ed = 0
    num_ppl = 0
    for i in range(len(df)):
        con = df.loc[i,'CON']
        if df.loc[i,'COUNTY'] not in \
            c2c[c2c['CON']==con]['HOME_COUNTY'].item().split(','):
            num_ed += 1
            num_ppl += df.loc[i,'POPULATION']
    return f_exp(num_ppl, num_ed, a, b)

#---------------------------------- CONTINUITY --------------------------------

#%% Continuity

def f_continuity(df, a=0.0001, b=0.01):
    '''
    Checks how much state has changed.
    '''
    data = df[df['CHANGE']>0]
    num_ed = len(data)
    num_ppl = data['POPULATION'].sum()
    return f_exp(num_ppl, num_ed, a, b)

#-------------------------------------- SER -----------------------------------

#%% 'Bump' Function

@jit(nopython=True)
def f(s, d=0.03):
    '''
    Bump function for each constituency.
    '''
    # Nearest integer to s - we want the SER to be an integer
    b = round(s)
    x = np.abs(s-b)
    if x == 0:
        return 1
    return 1 - np.exp(-d/x)

#%% SER Function

def f_ser(df, a=3, national_ratio=29800):
    '''
    Checks how desirable SER of all constituencies is.
    '''
    result = 0
    for c in np.unique(df['CON'].to_list()):
        s = ser(df, c, national_ratio)
        result += f(s)
    return a*result

#------------------------------ REWARD FUNCTION -------------------------------

#%% Reward

def reward(df, a_ser=3, a_cb=1e-10, b_cb=1e-4, a_cont=1e-3, b_cont=0.01,
           nr=29800):
    '''
    Reward function for dataframe df.
    '''
    if not f_contiguity(df):
        return 0 # No reward if not globally contiguous
    return f_county_boundary(df, c2c, a_cb, b_cb) + \
        f_continuity(df, a_cont, b_cont) + f_ser(df, a_ser, nr)
        