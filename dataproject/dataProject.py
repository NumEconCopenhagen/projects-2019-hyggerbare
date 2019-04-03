# Importing packages:
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import pandas_datareader
import datetime
import ipywidgets as widgets
from ipywidgets import interact

start = datetime.datetime(2005, 1, 1)
end   = datetime.datetime(2017, 1, 1)

# Fetching data from the Federal Reserve's API
cons  = pandas_datareader.data.DataReader('PCEC', 'fred', start, end) # Private consumption
inv   = pandas_datareader.data.DataReader('GPDI', 'fred', start, end) # Investments
publ  = pandas_datareader.data.DataReader('FGEXPND', 'fred', start, end) # Government expenditures
exp   = pandas_datareader.data.DataReader('NETEXP', 'fred', start, end) # Net exports

# Merging data from FED to dataframe
data_merged = pd.merge(cons, inv, how = 'left', on = ['DATE'])

for i in exp, publ:
    # i. merging remaining variables to dataframe
    data_merged = pd.merge(data_merged, i, how = 'left', on = ['DATE'])
    
# Defining names for columns
variable = {} 
variable['PCEC']    = 'Private Consumption'
variable['FGEXPND'] = 'Government Expenditures'
variable['GPDI']    = 'Investment'
variable['NETEXP']  = 'Net Exports'

# Renaming columns and calculating GDP as the sum of the former variables
data_merged.rename(columns = variable, inplace=True)
data_merged['Gross Domestic Product'] = data_merged.sum(axis = 1)

data_merged.describe()

# Creating an interactive figure with all time series

figure = plt.figure()
ax0    = data_merged.plot(grid = True)
plt.xlabel('Year')
plt.ylabel('Bil. $US (Current prices, seasonally adjusted)')

def draw(x):
    """ Function used in the interactive plot, showing either
        all series og chosen series.
    
    Args:
        x: series to plot
    
    Returns:
        plot: depending on chosen series, function returns a plot
        
    """
    if x == 'All': return figure
    else:  
        figure1 = plt.figure()
        ax0     = data_merged[x].plot(grid = True)
        plt.xlabel('Year')
        plt.ylabel('Bil. $US (Current prices, seasonally adjusted)')
        return plt.show() 

# Options for drop-down menu
Series = ['All', 'Gross Domestic Product', 'Private Consumption', 
          'Government Expenditures', 'Investment', 'Net Exports']    
interact(draw, x = Series)

# Creating shares of total GDP
ratios = data_merged.copy()
choose = ('Private Consumption', 'Investment','Net Exports', 'Government Expenditures')
for var in choose:
    # i. calculating ratios of total GDP for each variable
    ratios[var]    = ratios[var]/ratios['Gross Domestic Product']*100

# Plotting shares of GDP at different points in time
objects = ('Private Consumption', 'Investment', 'Net Exports', 'Government Expenditures')
y_pos = np.arange(len(objects))

for i in 0, 17, 36:    
    # i. defining the input to the bar chart
    performance = [ratios['Private Consumption'][i], ratios['Investment'][i], 
                   ratios['Net Exports'][i], ratios['Government Expenditures'][i]]
    
    # ii. plotting the bar chart, naming labels and title
    plt.figure()
    plt.bar(y_pos, performance, align = 'center', color = 'lightblue')
    plt.xticks(y_pos, objects)
    plt.ylabel('Percentage share of GDP')
    plt.title('Shares of total GDP '+str(ratios.index[i]))

data_merged_copy = data_merged.copy()

Liste = ['Gross Domestic Product', 'Private Consumption', 
         'Government Expenditures', 'Investment', 'Neat Exports']

for i in Liste:
    # i. percentage change of each variable
    data_merged_copy[i+'_Growth'] = data_merged_copy[i].pct_change()

# Multiplying 'Net Exports_Growth' column by -1 as we have learned that df.pct_change() 
# finds the right value but reversed (possibly due to the fact that Net Exports are negative).
data_merged_copy['Net Exports_Growth'] = data_merged_copy['Net Exports_Growth'].mul(-1)    
 
for i in Liste:    
    # i. mean of each variable
    data_merged_copy[i+' Mean'] = np.mean(data_merged_copy[i+'_Growth'])

# Plotting the quarterly growth rates seperately along with their mean
for i in Liste:
    plt.figure()
    plt.xlabel('Date')
    plt.ylabel('Quarterly Growth')
    ax1 = data_merged_copy[i+'_Growth'].plot(color='blue', grid = True, label = 'Quarterly growth')
    ax2 = data_merged_copy[i+' Mean'].plot(color='red', grid = True, label = 'Mean')
    plt.title(i+' (growth rate)')
    plt.show()