# convert from normal date time to julian date & Modified julian date
# Modified julian date is used at OMPS-LP data

import h5py
import numpy as np
import matplotlib.pyplot as plt

# the data from OMPS
file00 = 'OMPS-NPP_LP-L1G-EV_v2.5_2014m0219t072848_o11988_2016m0626t235315.h5'

filename = '../dat/'+file00

#ds_disk = xr.open_dataset(filename)
#print(ds_disk)

with h5py.File(filename, 'r') as data:
#    for group in data.keys() :
#        print (group)

    ds_date = data['GRIDDED_DATA']['Date'][()]
    ds_time = data['GRIDDED_DATA']['Time'][()]

ntime = 100 # OMPS event index
slit = 1 # central slit

date = ds_date[ntime,slit]
time = ds_time[ntime,slit]

print(date)

year = int(date/10000)
month = int((date - year*10000)/100)
day = date - year*10000 - month*100
print(year, month, day)
print(time)
hour = int(time/3600)
minute = int((time - hour * 3600)/60)
second = time - hour * 3600 - minute * 60

print(hour, minute, second)

# importing pandas as pd
import pandas as pd

# Create the Timestamp object
ts = pd.Timestamp(year = year,  month = month, day = day,
                  hour = hour, minute = minute, second = second, tz = 'UTC')

# Print the Timestamp object
print(ts)
print(ts.tz)

# convert to julian date
jd = ts.to_julian_date()
print(jd)

# convert to Modified julian date
mjd = jd - 2400000.5

print(mjd)

