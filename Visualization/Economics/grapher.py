# inflation_grapher.py
# graphs Inflation data from BLS.gov

import numpy
import matplotlib
from matplotlib import pyplot
import matplotlib.mlab as mlab
import pylab

# following two functions are helper functions before the data is graphed

# helper function to help with indexing through the data
# enumerate() takes two inputs: data & element.  If the data (within the
# parsed data file) matches an item that is defined in the main function,
# this function will return a tuple of an index number & the element
def getIndices(l, elem):
    return [i for i,x in enumerate(l) if x == elem]

# helper function to comb out the specific data we want to graph.  
def filter(data, item, area, frequency, adjusted):
    data_indices = getIndices(data['items'], item)
    item_indices = getIndices(data['area'], area)
    freq_indices = getIndices(data['reporting_frequency'], frequency)
    seasonal_indices = getIndices(data['sadjusted'], adjusted)
    indices = set(data_indices) & set(item_indices) & set(freq_indices) & set(seasonal_indices)
    ret_val = []
    for index in sorted(indices):
        ret_val.append(data[index])
    return ret_val

# matplotlib's csv reader function; loads into a numpy array
data = mlab.csv2rec('/Users/lynnroot/Desktop/WWC Python/session4/testdata.txt')

# reassigns data variable to only show my desired parameters
# here is where you can elect to filter out different parameters
# use the specific string names that are defined in your items.py and
# areas.py files
data = filter(data, 'All items', 'US City Average', 'M', 'S')

# fourth column in parsed data is year
def GetYear(item):
    return item[3]
    
# last column in parsed data is inflation value
def GetInflationValue(item):
    return item[-1]

# sets the min & max year that is within the data file;
# the min() & max() function is a part of python; we use the map() function
# to map the years from the filtered data
datemin = min(map(GetYear, data)) 
datemax = max(map(GetYear, data))

# number of months
interval = len(data) 

# linspace is a numpy function returns evenly spaced numbers based on
# a defined interval.  Here, it will create an x-axis of the minimum year and
# the maximum year within the data file, with the interval of data to be plot
# by months
x = numpy.linspace(datemin, datemax, interval)

# the actual data to be plot, mapping the inflation value function
# from the filtered data.
y = map(GetInflationValue, data)

# plot & show data
# notice that we don't have to do mlab.pyplot.plot here
# since we specifically imported pyplot in the beginning
pyplot.plot(x,y)
pyplot.show()