import os, sys
import numpy as np
from datetime import datetime
from matplotlib import pyplot
# set up import from file_parser
sys.path.insert(0, os.getcwd())# puts our other files on our python path
import file_parser as fp

def plot_simplehist(hours, xticks=None, title='San Francisco Crime Stats'):
    """ given an array of hours
    generate a histogram of frequency for each hour
    optional xticks to put hour (AM/PM) tickmarkes on x axis
    """
    pyplot.hist(hours, bins=100)
    pyplot.title(title)
    
    pyplot.ylabel('Number of Incidences')
    pyplot.xlabel('Hour (24 hour clock)')
    if not xticks == None:
        pyplot.xticks(xticks[0], xticks[1],rotation=45, fontsize='small')
    pyplot.grid()
    pyplot.show()


def make_xticks_24hours(nticks):
    """ returns ticks, labels for labelling an axis
    with nticks and labels
    Example
    -------
    make_xticks_24hours(2)
    ( [0,24], ['12 AM', '12 PM'] )
    """
    step = np.round(24/nticks)
    hourticks = np.arange(0,24,step)
    hourstr = [datetime(2012,1,1,x).strftime('%r') for x in hourticks]
    hourstr = [x.replace(':00:00','') for x in hourstr]
    return (hourticks, hourstr)
    
def get_sorted_label_instances(dict):
    """ given a dictionary of categories with lists of hours of occurances
    return a tuple of two lists
    (labels, ninstance)
    where labels are the names of the category
    ninstance = number of instances recorded"""
    labels = []
    ninstances = []
    for cat, hours in sorted(dict.items()):
        labels.append(cat)
        ninstances.append(len(hours))
    return (labels, ninstances)

    
def plot_pie(areas, labels, explode = None):
    """ generate a pie plot of relative number of event
    depicted by areas, as associated to category label in
    labels
    if explode  is True (default None)
    find largest region and emphasize
    """
    pyplot.figure(1, figsize=(10,10))
    pyplot.axes([0.1, 0.1, 0.8, 0.8])
    if explode:
        explode_ar = np.zeros(len(areas))# make zeros array size of areas
        explode_ar[np.argmax(areas)] = 0.05# set largest item to 0.05
    
    pyplot.pie(areas, labels=labels,shadow=True, explode = explode_ar)
    pyplot.show()


def radianlist_from_nxvals(n):
    """given a length n (depicting the number of x values in a list)
    generate equally spaced theta values in radians for use with
    a polar plot"""
    step = np.round(360/n) # calc step given number of samples
    values = np.arange(0,360,step)# make array of values 0->360 by step 
    theta = np.deg2rad(values) # cast to radians (from degrees)
    return theta


def stats_from_category_hours(dict, labels):
    """ returns a tuple containing
    (median value list, mean value list)
    in label order for each label in dict"""
    
    medians = []
    means = []
    for key in labels:
        vals = dict[key]
        medians.append(np.median(vals))
        means.append(vals.mean())
    return (medians, means)
    

def polar_plot(theta, r, size, labels):
    """ generate a polar plot
    theta = unique items in radians (eg like xticks)
    r = distance from center (eg median hour for category)
    size = size of point on plot (eg this will represent number of instances)
    labels = label for each point (in our case categories)
    """
    colors = theta # generate rainbow of colors
    scaled_size = np.array(size) * 100 # uniformly scale to make visible
    # set up figure
    pyplot.figure(1, figsize=(10,10))
    pyplot.axes([0.1, 0.1, 0.8, 0.8])
    pyplot.subplot(111, polar=True)
    pyplot.scatter(theta, r, c=colors, s=scaled_size)
    pyplot.xticks(theta, labels)
    pyplot.show()


if __name__ == '__main__':

    # use file_parser to get our data in a rec array
    data_file = 'sample_sfpd_incident_all.csv'
    full_datfile = fp.get_datafile(data_file)
    recdat = fp.data_from_csv2rec(full_datfile)
    # get all hours unspecified
    allhours = fp.hour_from_datrec(recdat)
    #plot_simplehist(allhours)

    # get category specific hours
    d_cathours = fp.categorymask_hours(recdat)
    

    # do some simple histogram plots
    # plot_simplehist(d_cathours['VEHICLE THEFT'], title='VEHICLE THEFT')
    # plot_simplehist(d_cathours['VEHICLE THEFT'], title='VEHICLE THEFT',
    #                 xticks = make_xticks_24hours(12))
    
    # get labels and number of instances for each category
    # to make a pie plot
    (labels, sizes) = get_sorted_label_instances(d_cathours)
    #plot_pie(sizes, labels, explode=True)
    
    ## set up data for a cool polar plot
    theta = radianlist_from_nxvals(len(sizes))
    medians, means = stats_from_category_hours(d_cathours, labels)
    
    #polar_plot(theta, medians, sizes, labels)
