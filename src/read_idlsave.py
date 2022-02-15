from os.path import dirname, join as pjoin
import scipy.io as sio
from scipy.io import readsav
import numpy as np

#data_dir = pjoin(dirname(sio.__file__), 'tests', 'data')
data_dir = './'

sav_fname = pjoin(data_dir, 'idl_filename.sav')

sav_data = readsav(sav_fname)

print(sav_data.keys())

print(np.shape(sav_data['variable_name']))

