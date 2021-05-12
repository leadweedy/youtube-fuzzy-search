## TO DO --------------------------------------------------------------

# things to do in the future (no particular order):

# implement command line inputs
# multithreading
# read more file types



## setup -----------------------------------------------------------

import urllib.request
import pandas
import re
import os
import random
import time
from configparser import ConfigParser


search_begin = 'https://www.youtube.com/results?search_query='
video_begin = 'https://www.youtube.com/watch?v='

# read from config file for initial conditions
config_object = ConfigParser()
config_object.read("config.ini")
# configure the csv info to read from config.ini
csv_data = config_object['CSV DATA']
csv_name = csv_data['file_name']
csv_columns = csv_data['column(s)']
start_element = csv_data['start']
# check if element is empty, default to 0
if not start_element:
    start_element = 0
# split columns into array and strip leading/trailing spaces
columns = csv_columns.split(',')
columns = [i.lstrip().rstrip() for i in columns]


## csv importer code ----------------------------------------------------

# imports data from csv into dataframe
import_data = pandas.read_csv(csv_name, header=0)

# set first column 
search_data = import_data[columns[0]]
# concatenate relevant search data for following columns (if any)
for i in range(1, len(columns)):
    search_data = search_data.str.cat(import_data[columns[i]], sep=' ')


## set up file export ----------------------------------------------------

# create text file named after the csv
base_filename = csv_name.replace('.csv','')
new_filename = base_filename
extension = '.txt'
# checks to see if file already exists
# if so, give the new file a (larger) unique number
i = 1
while os.path.isfile(new_filename + extension) == True:
    new_filename = base_filename + " (" + str(i) + ")"
    i += 1
# adds extension to filename
new_filename = new_filename + extension


## youtube fuzzy search code ---------------------------------------------

# iterate for each value
for i in range(0, len(search_data)):
    # update status
    print('Working on ' + str(i) + '/' + str(len(search_data)-1))
    # encode search query in utf8 so urllib doesnt break
    search_term = urllib.parse.quote(search_data.iloc[i], encoding='utf-8')
    # appends search term to end of youtube search url
    new_url = search_begin + search_term
    # scrapes html of youtube search page
    html = urllib.request.urlopen(new_url)
    # regex match the first video id from search results
    video_id = re.search(r"watch\?v=(\S{11})", html.read().decode())
    # generate full video url using id
    video_url = video_begin + video_id.group(1)
    # append video url to file
    with open(new_filename, 'a') as f:
        f.write(video_url)
        f.write('\n')
    # random delay between requests (max 1 second)
    time.sleep(random.random())


## cleanup ---------------------------------------------------------------
print('Done! ' + 'Filed saved to ' + new_filename)