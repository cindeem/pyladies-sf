# parses inflation data downloaded from bls.gov
# at ftp://ftp.bls.gov/pub/time.series/cu/cu.data.0.Current

from items import items # imports the items.py file we created
from area_names import names # imports the area_names.py file we created
import fileinput # for opening and reading the raw data file

# establish a counter
counter = 0

# iterate over each line of the raw data file
# input your own absolute directory path
for line in fileinput.input('/Users/lynnroot/desktop/wwc python/session4/rawdata.txt'):
    # skips over first line of column names
    if fileinput.isfirstline():
        continue

    # splits each line to identify columns
    splitline = line.rstrip().split('\t')
    
    # first column is the BLS series id
    series = splitline[0]
    
    # decode BLS series id column
    # cu = survey abbreviation; irrelevant
    # s = seasonally adjusted or unadjusted; relevant
    # r = reference base; irrelevant
    # area = area of survey
    # item = item surveyed
    cu, s, r, area, item = series[0:2],series[2],series[3],series[4:8],series[8:]
    
    # when looking at file, there is extra white space around items
    # strip items from extra white space
    item = item.strip()
    
    # regions
    area = names[area]
    
    # only care about items measured that are in items.py
    if (item not in items):
        continue
    # renames item code from name defined by items.py 
    item = items[item]

    # other columns
    # year measured is in column 2
    year = splitline[1]
    # strips extra white space
    year = year.lstrip().rstrip()
    
    # decode BLS periods in column 3
    # within data file, frequency: S = semiannual, M = monthly
    period = splitline[2]  
    frequency, pointinyear = period[0],period[1:]
    
    # inflation data in column 4
    value = splitline[3]
    # strips extra white space
    # can't remember why I chose r/lstrip() versus just strip()...
    value = value.lstrip().rstrip()

    # increase counter
    counter += 1

    # prints the data file using the decoded series IDs and separates it by
    # commas; converted counter from int to string  as the join() method
    # requires strings
    print ",".join([str(counter), item, area, year, s, frequency, pointinyear, value])