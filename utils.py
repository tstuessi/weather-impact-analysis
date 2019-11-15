'''
Utilities for analyzing the impact of local weather on car accident rates.

Developer: Tyler Stuessi (tylerstuessi@gmail.com)
'''

# base imports
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

import calendar

################################
# Convenient Plotting Wrappers
################################

def plot_time_hist(value_counts, title, xlabel=None, ylabel=None, figsize=(8,8), **kwargs):
    """Nicely plots time series counts using matplotlib. Passes defaults where necessary if none are supplied.
    
    Arguments:
        value_counts -- A pandas series containing the value counts for a particular time slice set.
        title -- Title of the plot
        xlabel -- Optional label for x axis
        ylabel -- Optional label for y axis
        figsize -- Optional figure size (same as matplotlib figsize)
    """
    # set up defaults if they aren't overridden
    if 'width' not in kwargs:
        kwargs['width'] = 1
    if 'edgecolor' not in kwargs:
        kwargs['edgecolor'] = 'black'

    # format the index nicely if it is a number (can assume it can be worked down to a float)
    if np.all(np.issubdtype(value_counts.index, np.number)):
        reordered = value_counts.sort_index()
        bar_x = reordered.index.astype('int')
        bar_vals = reordered.values
        x_tick_labels = bar_x
    else:
        bar_x = [0.5 + x for x in range(len(value_counts))]
        bar_vals = value_counts.values
        x_tick_labels = value_counts.index

    # plot values
    plt.figure(1, figsize=figsize)
    plt.bar(bar_x, bar_vals, **kwargs)
    
    # plot a mean line
    plt.plot(bar_x, [value_counts.mean()] * len(value_counts), '--', color='black', label='Mean')

    # update the formatting
    plt.title(title, fontsize=20)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=16)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=16)

    plt.xticks(bar_x, x_tick_labels, fontsize=12, rotation=45)
    plt.tick_params(axis='y', labelsize=12)
    plt.legend()

def plot_months_side_by_side(years, title, xlabel=None, ylabel=None, figsize=(8,8), **kwargs):
    """Plots the accident counts over the course of a year on the same plot.
    
    Arguments:
        years {list of (year, value_counts) pairs} -- The list of items that will be graphed.
        title {str} -- Title of the graph
    
    Keyword Arguments:
        xlabel {str} -- Label for the x axis (default: {None})
        ylabel {str} -- label for the y axis (default: {None})
        figsize {tuple} -- Figsize argument to pass to matplotlib (default: {(8,8)})
    """
    plt.figure(1, figsize=figsize)

    # plot the data
    for year, accident_series in years:
        plt.plot(accident_series.index, accident_series.values, '-o', label=year, **kwargs)
    
    # reformat the plot
    plt.title(title, fontsize=20)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=16)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=16)

    # resize y
    plt.ylim(bottom=500, top=2000)

    # convert the ticks
    plt.xticks(list(range(1, 13, 1)), [convert_month_to_abbr(month) for month in range(1, 13, 1)], rotation=45, fontsize=12)
    plt.tick_params(axis='y', labelsize=12)
    plt.legend()

def plot_days(years, title, xlabel=None, ylabel=None, figsize=(8,8), fit_trendline=False, deg=3, override_fit_color=None, **kwargs):
    plt.figure(1, figsize=figsize)
    plt.xticks(fontsize=12, rotation=45)
    plt.yticks(fontsize=12)

    # manually handle colors so we can plot trendlines along the way
    color_cycle_iter = iter(plt.rcParams['axes.prop_cycle'].by_key()['color'])
    for year, accident_series in years:
        year_color = next(color_cycle_iter)
        x_coords = np.array(range(len(accident_series)))
        plt.plot(x_coords,
                 accident_series.values, 
                 label=year,
                 color=year_color,
                  **kwargs)

        if fit_trendline:
            trendline = np.polyfit(x_coords, accident_series.values, deg)
            if override_fit_color is not None:
                fit_color = override_fit_color
            else:
                fit_color = year_color
            plt.plot(x_coords,
                    np.poly1d(trendline)(x_coords),
                    linewidth=2,
                    color=fit_color,
                    label='Least Squares fit with degree {}, year {}'.format(deg, year))

    # format plot
    plt.title(title, fontsize=20)
    if xlabel is not None:
        plt.xlabel(xlabel, fontsize=16)
    if ylabel is not None:
        plt.ylabel(ylabel, fontsize=16)
    
    plt.legend()

################################
# Data Cleaning Functions
################################

def convert_month_to_abbr(month):
    """Quick function to make month numbers more readable
    
    Arguments:
        month {number} -- Number from 1-12 identifying the month
    
    Returns:
        month_abbr {str} -- month abbreviation
    """
    return calendar.month_abbr[int(month)]