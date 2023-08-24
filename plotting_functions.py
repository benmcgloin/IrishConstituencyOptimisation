#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 11:05:56 2023

@author: elizasomerville
"""
#%% Imports

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import datetime
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator
import matplotlib.font_manager as font_manager
import tikzplotlib # To save plots as TikZ pictures

from data_analysis import ser_global

#%% Files

counties = gpd.read_feather('./data/county_data_simplified.feather')
bg = gpd.read_feather('./data/bg.feather')

#%% Palette
# Colour palette for plots

palette = [
    '#FBBC9E', # 1. Carlow-Kilkenny
    '#F89E79', # 2. Cavan-Monaghan
    '#EAE856', # 3. Clare
    '#F18E94', # 4. Cork East
    '#FFD88A', # 5. Cork North-Central
    '#95D6D7', # 6. Cork North-West
    '#FACFE2', # 7. Cork South-Central
    '#CFDF6A', # 8. Cork South-West
    '#F287B7', # 9. Donegal
    '#D293C1', # 10. Dublin Bay North
    '#DCE68B', # 11. Dublin Bay South
    '#B5B0D8', # 12. Dublin Central
    '#86D1D8', # 13. Dublin Fingal
    '#63C2A0', # 14. Dublin Mid-West
    '#FFEB94', # 15. Dublin North-West
    '#F287B7', # 16. Dublin Rathdown
    '#D0E28A', # 17. Dublin South-Central
    '#F9C0C2', # 18. Dublin South-West
    '#9FCF78', # 19. Dublin West
    '#8FB7E1', # 20. Dún Laoghaire
    '#F598A4', # 21. Galway East
    '#FDC896', # 22. Galway West
    '#F7AEBE', # 23. Kerry
    '#D293C1', # 24. Kildare North
    '#EFBED9', # 25. Kildare South
    '#94CC7D', # 26. Laois-Offaly
    '#F89E79', # 27. Limerick City
    '#67C18C', # 28. Limerick County
    '#FFEB94', # 29. Longford-Westmeath
    '#63C2A0', # 30. Louth
    '#A2DCED', # 31. Mayo
    '#F7A6AD', # 32. Meath East
    '#9FDBED', # 33. Meath West
    '#44BEAA', # 34. Roscommon-Galway
    '#E4EB9E', # 35. Sligo-Leitrim
    '#B5B0D8', # 36. Tipperary
    '#E4EB9E', # 37. Waterford
    '#6ABACF', # 38. Wexford
    '#FFE96B', # 39. Wicklow
]

#%%
def tikzplotlib_fix_ncols(obj):
    """
    Workaround for matplotlib 3.6 renamed legend's _ncol to _ncols, 
    which breaks tikzplotlib.
    """
    if hasattr(obj, "_ncols"):
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)

#%% SER Table

def make_ser_table(df, name='table', dpi=300, save_tex=False):
    '''
    Creates a table showing the SER of each CT.
    '''
    ser_dictionary = ser_global(df)
    fig, ax = plt.subplots()
    
    # Hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    
    # Get SER data
    table_data = pd.DataFrame.from_dict([ser_dictionary]).T
    table_data = table_data.reset_index()
    table_data.columns = ['Constituency','SER']
    table_data['Constituency'] = table_data['Constituency'].str.title()
    table_data = table_data.round(3)
    table_data['SER'] = table_data['SER'].apply('{:0<5}'.format)
    
    if save_tex:
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        # Save data to TeX
        table_data.to_latex(f'./{name}_{time}.tex', index=False)
    
    t = ax.table(
        cellText=table_data.values, 
        colLabels=table_data.columns, 
        loc='center',
        colWidths=[0.4,0.2],
        cellLoc='left'
        )
    t.scale(1, 2)
    t.set_fontsize(15)
    
    # Get current time
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    fig.savefig(f'./images/{name}_{time}.png', dpi=dpi, bbox_inches='tight')
    
#%% SER Chart

def make_ser_chart(df1, df2, name='chart', dpi=300, filetype='png', 
                   save_tex=False):
    '''
    Creates a bar chart comparing the SER of each CT for two states.
    Saves a PNG by default.
    '''
    
    # Create dictionaries of SER values for each CT
    ser_dictionary_1 = ser_global(df1)
    ser_dictionary_2 = ser_global(df2)
    
    # Create dataframes from dictionaries
    data_1 = pd.DataFrame.from_dict([ser_dictionary_1])
    data_2 = pd.DataFrame.from_dict([ser_dictionary_2])
    
    # Concatenate dataframes, reset index, and transpose
    data = pd.concat([data_1, data_2]).reset_index(drop=True).T
    data.index = data.index.set_names('Constituency')
    data.index = pd.Series(data.index.values).str.title()
    # Label datasets
    data = data.rename({0:'Original',1:'Optimal'}, axis=1)
    
    # Round to three decimal places
    data = data.round(3)
    
    data['Original'] = data['Original'].apply('{:0<5}'.format).astype('float64')
    data['Optimal'] = data['Optimal'].apply('{:0<5}'.format).astype('float64')
    
    fig, ax = plt.subplots(1, 1, figsize=(15, 11))
    
    # Plot horizontal lines at integer values
    ax.hlines(
        [1,2,3,4,5], 
        xmin=0, 
        xmax=50, 
        colors='darkgrey', 
        zorder=0
        )
    
    # Plot bar chart
    data.plot.bar(
        rot=0, 
        ax=ax, 
        zorder=1, 
        alpha=0.9,
        color=['powderblue', 'steelblue']
        )
    
    # Label axes
    ax.set_xlabel('Constituency', fontsize=15)
    ax.set_ylabel('SER', fontsize=15)
    
    # Restrict y axis
    ax.set_ylim(2,6)
    # Only plot tick labels at integer values
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    # Plot vertical bar labels
    plt.setp(
        ax.get_xticklabels(), 
        fontsize=12, 
        rotation='vertical'
        )
    
    font = font_manager.FontProperties(
        style='normal', 
        size=16
        )
    ax.legend(prop=font)
    
    if save_tex:
        fig = plt.gcf()
        tikzplotlib_fix_ncols(fig)
        tikzplotlib.clean_figure()
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        tikzplotlib.save(f'ser_CT_{time}.tex')
    
    # Get current time
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    if filetype == 'png':
        fig.savefig(f'./images/{name}_{time}.png', dpi=dpi, bbox_inches='tight')
    else:
        fig.savefig(f'./images/{name}_{time}.{filetype}', bbox_inches='tight',
                    transparent=True, pad_inches=0)
    
#%% Plot

def make_plot(df, name='plot', dpi=500, legend=True, filetype='png'):
    '''
    Creates a plot of EDs coloured according to CT.
    Saves a PNG by default.
    '''
    fig, ax = plt.subplots(1, 1, figsize=(11, 11))
    
    # Plot EDs coloured according to CT
    df.plot(
        column='CON', 
        cmap=ListedColormap(palette), 
        ax=ax, 
        categorical=True, 
        legend=legend
        )
    
    if legend:
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.85, 0.5, 0.5, 0.5))
        
    # Remove axes and tick labels
    ax.set_axis_off()
    ax.tick_params(
        axis='both',        # Affect both the x and y axes
        which='both',       # Get rid of both major and minor ticks
        top=False,          # Get rid of ticks on top/bottom/left/right
        bottom=False,
        left=False,
        right=False,
        labeltop=False,     # Get rid of labels on top/bottom/left/right
        labelbottom=False,
        labelleft=False,
        labelright=False
        )
    
    # Get current time
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    if filetype == 'png':
        fig.savefig(f'./images/{name}_{time}.png', dpi=dpi, bbox_inches='tight',
                    transparent=True)
    else:
        fig.savefig(f'./images/{name}_{time}.{filetype}', bbox_inches='tight',
                    transparent=True, pad_inches=0)
    
#%% County Boundary Plot

def make_county_boundary_plot(df, name='plot', dpi=500, x=11, y=11, filetype='png'):
    '''
    Creates a plot of EDs coloured according to CT, overlaid with county
    boundaries.
    Saves a PNG by default.
    '''
    fig, ax = plt.subplots(1,1,figsize=(x,y))
    #fig.set_facecolor('lightgrey')
    #ax.set_facecolor('lightgrey')
    # Plot background colour
    bg.plot(
        facecolor='none',
        edgecolor='grey', 
        ax=ax, 
        linewidth=2
        )
    
    # Plot EDs coloured according to CT
    df.plot(
        column='CON',
        cmap=ListedColormap(palette), 
        ax=ax, 
        categorical=True, 
        legend=True
        )
    
    # Plot county boundaries on top
    counties.plot(
        facecolor='none', 
        edgecolor='grey', 
        ax=ax
        )
    
    leg = ax.get_legend()
    leg.set_bbox_to_anchor((0.9, 0.5, 0.5, 0.5))
    
    # Remove axes and tick labels
    ax.set_axis_off()
    ax.tick_params(
        axis='both',        # Affect both the x and y axes
        which='both',       # Get rid of both major and minor ticks
        top=False,          # Get rid of ticks on top/bottom/left/right
        bottom=False,
        left=False,
        right=False,
        labeltop=False,     # Get rid of labels on top/bottom/left/right
        labelbottom=False,
        labelleft=False,
        labelright=False
        )
    
    # Get current time
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    if filetype == 'png':
        fig.savefig(f'./images/{name}_county_boundary_{time}.png', dpi=dpi, 
                    bbox_inches='tight', transparent=True)
    else:
        fig.savefig(f'./images/{name}_county_boundary_{time}.{filetype}', bbox_inches='tight',
                    transparent=True, pad_inches=0)
    