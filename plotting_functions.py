#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 28 11:05:56 2023

@author: elizasomerville
"""
# =============================================================================
#                          PLOTTING FUNCTIONS
# =============================================================================

#%% Imports

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import datetime
import tikzplotlib # To save plots as TikZ pictures

from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator

from data_analysis import ser_global, vna_global

#%% Files

counties = gpd.read_feather('./data/IrishCountiesSimplified.feather')
bg = gpd.read_feather('./data/IrelandCoastline.feather') # Outline of Ireland
dublin_outline = counties[counties.index=='DUBLIN']
con_outlines = gpd.read_feather('./data/IrishConstituencies.feather')

#%% Palette
# Colour palette for plots

palette = [
    '#F89E79', #  1. Carlow-Kilkenny
    '#FBBC9E', #  2. Cavan-Monaghan
    '#EAE856', #  3. Clare
    '#F18E94', #  4. Cork East
    '#FFD88A', #  5. Cork North-Central
    '#95D6D7', #  6. Cork North-West
    '#FACFE2', #  7. Cork South-Central
    '#CFDF6A', #  8. Cork South-West
    '#F287B7', #  9. Donegal
    '#D293C1', # 10. Dublin Bay North
    '#ECF794', # 11. Dublin Bay South
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

cons = ['CARLOW-KILKENNY', 'CAVAN-MONAGHAN', 'CLARE', 'CORK EAST',
       'CORK NORTH-CENTRAL', 'CORK NORTH-WEST', 'CORK SOUTH-CENTRAL',
       'CORK SOUTH-WEST', 'DONEGAL', 'DUBLIN BAY NORTH',
       'DUBLIN BAY SOUTH', 'DUBLIN CENTRAL', 'DUBLIN FINGAL',
       'DUBLIN MID-WEST', 'DUBLIN NORTH-WEST', 'DUBLIN RATHDOWN',
       'DUBLIN SOUTH-CENTRAL', 'DUBLIN SOUTH-WEST', 'DUBLIN WEST',
       'DÚN LAOGHAIRE', 'GALWAY EAST', 'GALWAY WEST', 'KERRY',
       'KILDARE NORTH', 'KILDARE SOUTH', 'LAOIS-OFFALY', 'LIMERICK CITY',
       'LIMERICK COUNTY', 'LONGFORD-WESTMEATH', 'LOUTH', 'MAYO',
       'MEATH EAST', 'MEATH WEST', 'ROSCOMMON-GALWAY', 'SLIGO-LEITRIM',
       'TIPPERARY', 'WATERFORD', 'WEXFORD', 'WICKLOW']

color_dict = {con:color for con, color in zip(cons, palette)}

palette_dublin = palette[9:20]

plt.rcParams['figure.dpi'] = 300

#%%
def create_proxy(label):
    '''
    Create a proxy image to display custom labels in legend.
    Used in make_full_plot for numeric legend.
    '''
    # For one-digit numbers, marker size should be smaller
    ms = 1.9 if int(label) < 10 else 3
        
    line = matplotlib.lines.Line2D(
        [0], 
        [0], 
        linestyle='none', 
        mfc='black',
        mec='none', 
        marker=r'$\mathregular{{{}}}$'.format(label),
        markersize=ms
        )
    
    return line

#%%
def numbered_con_dict(df):
    '''
    Returns dictionary with constituency:number pairs, 
    in alphabetical order.
    '''
    cons = np.unique(df['CON'].str.title())
    con_dict = {cons[i]:i+1 for i in range(len(cons))}
    return con_dict

#%%
def tikzplotlib_fix_ncols(obj):
    '''
    Workaround for matplotlib 3.6 renamed legend's _ncol to _ncols, 
    which breaks tikzplotlib.
    '''
    if hasattr(obj, "_ncols"):
        obj._ncol = obj._ncols
    for child in obj.get_children():
        tikzplotlib_fix_ncols(child)

#%% SER Table

def make_ser_and_vna_table(df, name='table', dpi=300, save_tex=False, 
                           seats=False, use_current_seats=False):
    '''
    Creates a table showing the SER and VNA of each CON.
    If use_current_seats=True, then use currently assigned seat numbers
    to compute VNA.
    If seats=True, add a column showing seats assigned to each CON.
    '''
    ser_dictionary = ser_global(df)
    vna_dictionary = vna_global(df, use_current_seats)
    
    fig, ax = plt.subplots()
    
    # Hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    
    # Get SER data
    table_data = pd.DataFrame.from_dict([ser_dictionary]).T
    table_data = table_data.reset_index()
    table_data.columns = ['Constituency','SER']
    table_data['VNA'] = table_data['Constituency'].map(vna_dictionary)
    table_data['Constituency'] = table_data['Constituency'].str.title()
    table_data = table_data.round(3)
    table_data['SER'] = table_data['SER'].apply('{:0<5}'.format)
    table_data['VNA'] = table_data['VNA'].apply('{:0<5}'.format)
    
    if seats:
        if use_current_seats:
            # Get current seat numbers from dataframe
            table_data['Seats'] = list(df.groupby('CON').first()['SEATS'])
        else:
            # Compute seat number by rounding SER
            table_data['Seats'] = np.round(table_data['SER']
                                           .apply(float)).apply(int)
        table_data = table_data[['Constituency', 'Seats', 'SER', 'VNA']]
        col_widths =[0.4,0.2,0.2,0.2]
    else:
        col_widths =[0.4,0.2,0.2]
    
    if save_tex:
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        # Save data to TeX
        table_data.to_latex(f'./tex/{name}_{time}.tex', index=False)
    
    t = ax.table(
        cellText=table_data.values, 
        colLabels=table_data.columns, 
        loc='center',
        colWidths=col_widths,
        cellLoc='left'
        )
    t.scale(1, 2)
    t.set_fontsize(15)
    
    # Get current time
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    fig.savefig(f'./images/{name}_{time}.png', dpi=dpi, bbox_inches='tight')
    
#%% SER Chart

def format_chart_data(df1, df2, metric='SER', 
                      use_current_seats_for_current=True):
    '''
    Returns a dataframe indexed by constituency, with columns corresponding
    to SER/VNA of the original and optimal configurations.
    '''
    if metric == 'SER':
        # Create dictionaries of SER values for each CON
        dictionary_1 = ser_global(df1)
        dictionary_2 = ser_global(df2)
    elif metric == 'VNA':
        # Create dictionaries of VNA values for each CON
        dictionary_1 = vna_global(df1, use_current_seats_for_current)
        dictionary_2 = vna_global(df2)
    
    # Create dataframes from dictionaries
    data_1 = pd.DataFrame.from_dict([dictionary_1])
    data_2 = pd.DataFrame.from_dict([dictionary_2])
    
    # Concatenate dataframes, reset index, and transpose
    data = pd.concat([data_1, data_2]).reset_index(drop=True).T
    data.index = data.index.set_names('Constituency')
    data.index = pd.Series(data.index.values).str.title()
    # Label datasets
    data = data.rename({0:'Original',1:'Optimal'}, axis=1)
    
    # Round to three decimal places
    data = data.round(3).abs()
    
    data['Original'] = data['Original'].apply(
        '{:0<5}'.format).astype('float64')
    data['Optimal'] = data['Optimal'].apply(
        '{:0<5}'.format).astype('float64')

    return data

#%%

def make_chart(df1, df2, name='chart', dpi=300, x=15, y=11, filetype='png', 
                   save_tex=False, metric='SER', 
                   use_current_seats_for_current=True):
    '''
    Creates a bar chart comparing the SER/VNA of each CON for two states.
    Saves a PNG by default, otherwise PDF.
    '''
    # Get formatted chart data
    data = format_chart_data(df1, df2, metric, use_current_seats_for_current)

    fig, ax = plt.subplots(1, 1, figsize=(x,y))
    
    if metric=='SER':
        # Plot horizontal lines at integer values
        ax.hlines(
            [1,2,3,4,5], 
            xmin=0, 
            xmax=50, 
            colors='darkgrey', 
            zorder=0
            )
    elif metric=='VNA':
        ax.hlines(
            [0.05],
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
    ax.set_ylabel(metric, fontsize=15)
    
    if metric == 'SER':
        # Restrict y axis
        ax.set_ylim(2,6)
        # Only plot tick labels at integer values
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    # Plot vertical bar labels on the x axis
    plt.setp(
        ax.get_xticklabels(), 
        fontsize=12, 
        rotation='vertical'
        )
    
    # Set legend font size
    font = matplotlib.font_manager.FontProperties(
        style='normal', 
        size=16
        )
    ax.legend(prop=font)
    
    if save_tex:
        fig = plt.gcf()
        tikzplotlib_fix_ncols(fig) # Fix naming issue in tikzplotlib
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        tikzplotlib.save(f'./tex/{name}_{metric}_{time}.tex')
    
    # Get current time
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    if filetype.upper().strip() == 'PNG':
        fig.savefig(
            f'./images/{metric}_{name}_{time}.png', 
            dpi=dpi, 
            bbox_inches='tight'
            )
    elif filetype.upper().strip() == 'PDF':
        fig.savefig(
            f'./images/{metric}_{name}_{time}.pdf', 
            bbox_inches='tight',
            transparent=True, 
            pad_inches=0
            )
    else:
        print('Only filetypes PNG and PDF currently supported.')
        
#%% SER Chart

def make_double_chart(df1, df2, name='chart', dpi=300, x=15, y=20, 
                      filetype='png', save_tex=False,
                      use_current_seats_for_current=True):
    '''
    Creates a bar chart comparing the SER/VNA of each CON for two states.
    Saves a PNG by default, otherwise PDF.
    '''
    # Get formatted chart data
    ser_data = format_chart_data(
        df1, 
        df2, 
        metric='SER'
        )
    vna_data = format_chart_data(
        df1,
        df2, 
        metric='VNA', 
        use_current_seats_for_current=use_current_seats_for_current
        )
    
    fig, axs = plt.subplots(2, 1, figsize=(x,y))
    
    # Horizontal lines at integers for SER chart
    axs[0].hlines(
        [1,2,3,4,5], 
        xmin=0, 
        xmax=50, 
        colors='darkgrey', 
        zorder=0
        )
    # Horizontal line at threshold value of 0.05 for VNA chart
    axs[1].hlines(
        [0.05],
        xmin=0, 
        xmax=50, 
        colors='darkgrey', 
        zorder=0
        )

    # Plot SER bar chart
    ser_data.plot.bar(
        rot=0, 
        ax=axs[0], 
        zorder=1, 
        alpha=0.9,
        color=['powderblue', 'steelblue']
        )
    
    # Plot VNA bar chart
    vna_data.plot.bar(
        rot=0, 
        ax=axs[1], 
        zorder=2, 
        alpha=0.9,
        color=['powderblue', 'steelblue'],
        legend=False
        )
    
    # Label axes
    for i in range(2):
        # Plot vertical bar labels on x axes of both plots
        plt.setp(
            axs[i].get_xticklabels(), 
            fontsize=12, 
            rotation='vertical'
            )
    
    # Other settings for SER chart
    axs[0].set_ylabel('SER', fontsize=15)
    # Restrict y axis
    axs[0].set_ylim(2,6)
    # Only plot tick labels at integer values
    axs[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    # Set legend font
    font = matplotlib.font_manager.FontProperties(
        style='normal', 
        size=16
        )
    axs[0].legend(prop=font)
    
    # Other settings for VNA chart
    axs[1].set_xlabel('Constituency', fontsize=15)
    axs[1].set_ylabel('VNA', fontsize=15)
    
    plt.tight_layout()
    
    if save_tex:
        fig = plt.gcf()
        tikzplotlib_fix_ncols(fig) # Fix naming issue in tikzplotlib
        tikzplotlib.clean_figure()
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        tikzplotlib.save(f'./tex/comp_chart_{time}.tex')
    
    # Get current time
    time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    
    if filetype.upper().strip() == 'PNG':
        fig.savefig(
            f'./images/{name}_{time}.png', 
            dpi=dpi, 
            bbox_inches='tight'
            )
    elif filetype.upper().strip == 'PDF':
        fig.savefig(
            f'./images/{name}_{time}.pdf', 
            bbox_inches='tight',
            transparent=True, 
            pad_inches=0
            )
    else:
        print('Only filetypes PNG and PDF currently supported.')
    
#%% Plot
            
def make_plot(df_orig, name='plot', dpi=500, legend=True, x=11, y=11,
              filetype='png', numbered=False, save=True, ax=None,
              outline_dublin=False, highlight_changes=False):
    '''
    Creates a plot of EDs coloured according to CON.
    If save=True, then saves a PNG/PDF depending on filetype.
    If save=False, ax can be passed for plotting.
    If highlight_changes=True, then changed EDs are highlighted.
    '''
    if ax == None:
        # If not plotting on an existing axis, then create a new figure
        fig, ax = plt.subplots(1, 1, figsize=(x,y))
    
    df = df_orig.copy()
    
    df['CON'] = df['CON'].str.title()
    
    if highlight_changes:
        con_outlines.plot(
            facecolor='grey',
            edgecolor='darkgrey',
            ax=ax
            )
        
        changed = df[df['CHANGE']>0]
        changed['CON'] = changed['CON'].str.upper()
        changed['COLOR'] = changed['CON'].map(color_dict)
        changed.plot(color=changed['COLOR'], ax=ax)
        
        legend=False
    else:
        # Plot EDs coloured according to CON
        df.plot(
            column='CON', 
            cmap=ListedColormap(palette), 
            ax=ax, 
            categorical=True, 
            legend=legend
            )
        
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
    
    if numbered:
        cons = np.unique(df[df['COUNTY']!='DUBLIN']['CON'])
        nums = numbered_con_dict(df)
    
        for c in cons:
            # Get centroid of each constituency
            pt_xy = gpd.GeoSeries(df[df['CON']==c].unary_union.centroid)
            pt = (pt_xy.x, pt_xy.y)
            # Annotate with number at centroid
            ax.annotate(
                text=nums[c], 
                xy=pt, 
                ha='center', 
                fontsize=3,
                bbox={'boxstyle':'circle','color':'white'}
                )
        
        if save:
            labels = [nums[c] for c in cons]
            proxies = [create_proxy(num) for num in labels]
            ax.legend(proxies, cons, numpoints=1, markerscale=2)
            
    if outline_dublin:
        dublin_outline.plot(
            ax=ax, 
            facecolor='none', 
            edgecolor='grey',
            linewidth=0.5
            )
        
    if legend:
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.85, 0.5, 0.5, 0.5))
    
    if save:
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        
        if filetype.upper().strip() == 'PNG':
            fig.savefig(
                f'./images/{name}_{time}.png', 
                dpi=dpi, 
                bbox_inches='tight',
                transparent=True
                )
        elif filetype.upper().strip() == 'PDF':
            fig.savefig(
                f'./images/{name}_{time}.pdf', 
                bbox_inches='tight',
                transparent=True, 
                pad_inches=0
                )
        
#%% Plot

def make_dublin_plot(df_orig, name='plot', dpi=500, legend=True, x=11, y=11,
              filetype='png', numbered=False, save=True, ax=None):
    '''
    Creates a plot of EDs coloured according to CON.
    Saves a PNG by default, otherwise PDF.
    '''
    if ax == None:
        # If not plotting on an existing axis, then create a new figure
        fig, ax = plt.subplots(1, 1, figsize=(x,y))
    
    df = df_orig.copy()
    df['CON'] = df['CON'].str.title()
    
    dub = df[df['COUNTY']=='DUBLIN']
    
    # Plot EDs coloured according to CON
    dub.plot(
        column='CON', 
        cmap=ListedColormap(palette_dublin), 
        ax=ax, 
        categorical=True, 
        legend=legend
        )
        
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
    
    if numbered:
        cons = np.unique(dub['CON'])
        nums = numbered_con_dict(df)
    
        for c in cons:
            # Get centroid of each constituency
            pt_xy = gpd.GeoSeries(df[df['CON']==c].unary_union.centroid)
            pt = (pt_xy.x, pt_xy.y)
            # Annotate with number at centroid
            ax.annotate(
                text=nums[c], 
                xy=pt, 
                ha='center', 
                fontsize=3,
                bbox={'boxstyle':'circle','color':'white'}
                )
        
        if save:
            labels = [nums[c] for c in cons]
            proxies = [create_proxy(num) for num in labels]
            ax.legend(proxies, cons, numpoints=1, markerscale=2)
        
    if legend:
        leg = ax.get_legend()
        leg.set_bbox_to_anchor((0.85, 0.5, 0.5, 0.5))
            
    if save:
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        
        if filetype.upper().strip() == 'PNG':
            fig.savefig(
                f'./images/{name}_{time}.png', 
                dpi=dpi, 
                bbox_inches='tight',
                transparent=True
                )
        elif filetype.upper().strip() == 'PDF':
            fig.savefig(
                f'./images/{name}_{time}.pdf', 
                bbox_inches='tight',
                transparent=True, 
                pad_inches=0
                )
        else:
            print('Only filetypes PNG and PDF currently supported.')
            
#%%
def make_legend(df_orig, ax):
    '''
    Creates a numbered legend for the 39 constituencies.
    '''
    ax.set_aspect(2)
    ax.margins(0,0)
    # Remove axes
    ax.set_axis_off()
    
    df = df_orig.copy()
    df['CON'] = df['CON'].str.title()
    # Constituencies
    cons = np.unique(df['CON'])
    # Constituency-number dictionary
    nums = numbered_con_dict(df)
    # Numbers corresponding to constituencies
    labels = [nums[c] for c in cons]
    # Create legend images showing numbers
    proxies = [create_proxy(num) for num in labels]
    
    # Plot legend
    ax.legend(
        proxies, 
        cons, 
        numpoints=1, 
        markerscale=1, 
        fontsize=3, 
        loc='upper right',
        bbox_to_anchor=(1,0.97), 
        borderpad=0.8
        )
    # Set width of legend frame
    leg = ax.get_legend()
    leg.get_frame().set_linewidth(0.2)
    
#%%
def make_full_plot(df, save=True):
    '''
    Make a numbered plot showing all Irish constituencies,
    including a zoomed view of Dublin.
    '''
    # A = Full country plot
    # B = Zoomed view of Dublin
    # C = Custom numbered legend
    mosaic_layout = '''
    AAAC
    AAAC
    AAAC
    BBBC
    BBBC
    '''
    fig, axs = plt.subplot_mosaic(mosaic_layout)
    plt.subplots_adjust(wspace=-0.91, hspace=0)
    # Plot A
    make_plot(
        df,
        legend=False,
        numbered=True,
        save=False,
        ax=axs['A'],
        outline_dublin=True
        )
    # Plot B
    make_dublin_plot(
        df, 
        legend=False,
        numbered=True, 
        save=False,
        ax=axs['B']
        )
    # Plot C
    make_legend(
        df, 
        ax=axs['C']
        )
    plt.margins(0,0)
    
    if save:
        # Get current time
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        
        fig.savefig(f'./images/full_plot_{time}.png', 
                    dpi=500,
                    bbox_inches='tight',
                    transparent=True, 
                    pad_inches=0.1
                    )
        
#%% County Boundary Plot

def make_county_boundary_plot(df_orig, name='plot', dpi=500, x=11, y=11, 
                              filetype='png'):
    '''
    Creates a plot of EDs coloured according to CON, overlaid with county
    boundaries.
    Saves a PNG by default, otherwise PDF.
    '''
    fig, ax = plt.subplots(1,1,figsize=(x,y))
    
    df = df_orig.copy()
    df['CON'] = df['CON'].str.title()
    
    # Plot background colour
    bg.plot(
        facecolor='none',
        edgecolor='grey', 
        ax=ax, 
        linewidth=2
        )
    
    # Plot EDs coloured according to CON
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
    
    if filetype.upper().strip() == 'PNG':
        fig.savefig(
            f'./images/{name}_county_boundary_{time}.png', 
            dpi=dpi, 
            bbox_inches='tight', 
            transparent=True
            )
    elif filetype.upper().strip() == 'PDF':
        fig.savefig(
            f'./images/{name}_county_boundary_{time}.pdf', 
            bbox_inches='tight',
            transparent=True, 
            pad_inches=0
            )
    else:
        print('Only filetypes PNG and PDF currently supported.')
    