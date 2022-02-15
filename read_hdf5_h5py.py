import numpy as np
import h5py

path1 = './dat/'
filename1 = 'filename.h5'

with h5py.File(path1+filename1, 'r') as data:
#    for group in data.keys() :
#        print (group)

# adding [()]
# because When we assign f['default'] to the variable data.
# We are not reading the data from the file.
# Instead, we are generating a pointer to where the data is located on the hard drive.
    scale = data['.']['variable_name'].attrs['scale_factor']
    offset = data['.']['variable_name'].attrs['add_offset']
    ds_data = data['.']['variable_name'][()]
    print (ds_data.shape, ds_data.dtype)
    var1 = (ds_data - offset)* scale
    ds_data1 = data['.']['latitude'][()]
    print (ds_data1.shape, ds_data1.dtype)
    ds_data2 = data['.']['longitude'][()]
    print (ds_data2.shape, ds_data2.dtype)

lat = ds_data1[:,:].flatten()
lon = ds_data2[:,:].flatten()
data = var1[:,:].flatten()

