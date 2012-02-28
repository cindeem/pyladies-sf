import os
import numpy as np
from datetime import datetime
from matplotlib import pyplot
from matplotlib.mlab import csv2rec
import csv
from numpy.testing import (assert_raises, assert_equal)


def get_datafile(filename):
    """looks in relative data directory for <filename>
    raises error if not found
    else returns full path to file"""

    # set up relative import of data                                                 
    cwd = os.getcwd()
    base_path , _ = os.path.split(cwd)
    data_dir = os.path.join(base_path, 'data') 
    fullfile = os.path.join(data_dir, filename)
    if not os.path.isfile(fullfile):
        raise IOError('%s was not found in %s'%(filename, data_dir))
    return fullfile


def data_from_loadtxt(infile, delimiter=','):
    """ Uses numpy loadtext to try to load <infile>
    using data-type string  dtype=str
    and using specified delimiter (default =  ','; comma)
    """
    dat = np.loadtxt(infile, dtype=str, delimiter=delimiter)
    return dat

def data_from_csv(infile):
    """Uses csv package to read file and create dictionary giving
    header = [list of values]""" 
    csvdat = csv.reader(open(infile))
    csv_headers = csvdat.next() # grab first row from file to get headers            
    # initialize dictionary where keys= header names, default value is a list        
    csvd = {}
    for item in csv_headers:
        csvd[item] = []
    for row in csvdat: # iterate through the rest of the file                        
        for val, header_name in enumerate(csv_headers):
            csvd[header_name].append(row[val])
            print val, header_name
    return csvd


def data_from_csv2rec(infile):
    """Uses matplotlib.mlab csv2rec to parse data
    trys to cast fildes into correct data-type
    datrec.dtype to see datat-types and names
    """
    datrec = csv2rec(infile)
    return datrec 

def hour_from_datrec(datrec):
    hours = [x.hour for x in datrec['time']]
    return np.array(hours)

def category_mask(datrec, category):
    categories = set(datrec['category'])
    if not category in [x for x in categories]:
        raise IOError('category %s not in %s'%(category, categories))
    mask = datrec['category'] == category
    return mask

def categorymask_hours(datrec):
    """ for each unique category in datrec,
    masks data and returns dictionary:
    category = [list of hours]"""
    categories = set(datrec['category'])
    outd = {}
    hours =  hour_from_datrec(datrec)
    for category in categories:
        cat_mask = category_mask(datrec, category)
        cat_hours = hours[cat_mask]
        outd[category] = cat_hours
    return outd



if __name__ == '__main__':

    #specify datafile
    data_file = 'sample_sfpd_incident_all.csv'

    # test that data file will be found
    assert_raises(IOError, get_datafile, 'nofile.csv')
    #assert_raises(IOError, get_datafile, data_file)
    # you can uncomment the above test to see that it fails
    cwd = os.getcwd()
    tmp_datafile = '../data/sample_sfpd_incident_all.csv'
    tmp_fulldatafile = os.path.abspath(os.path.join(cwd, tmp_datafile))
    #note that I need to get the abs filepath to match with what get_datafile gives me  
    assert_equal(tmp_fulldatafile, get_datafile(data_file))

    # test data_from_csv
    dataf = get_datafile(data_file)
    csv_dat = data_from_csv(dataf)
    assert_equal('Category', sorted(csv_dat.keys())[0])
    assert_equal(99, len(csv_dat['Category']))# each category has 99 items in its list

    # test csv2rec
    recdat = data_from_csv2rec(dataf)
    dtype_names = recdat.dtype.names
    assert_equal('incidntnum', dtype_names[0])

    # test category_mask(datrec, category)
    categories = set(recdat['category'])
    tmpcat = [x for x in categories]
    cat_mask = category_mask(recdat, tmpcat[0])
    # assert that the mask is an array of bools (np.bool_)
    assert_equal(np.bool_, type(cat_mask[0]))
    assert_equal(np.array([True, False]), cat_mask[:2])
    
    # test category_hours
    d_cathours = categorymask_hours(recdat)
    assert_equal(np.array([8]), d_cathours['WEAPON LAWS'])
