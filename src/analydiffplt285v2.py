"""
used for comparing the difference of 2 granules after removing 285K pixels
compare 3 datasets
1) MODIS
2) RROCI
3) RROCI ADDED NOISE

no plotting needed this code

xarray -> dataarray -> numpy array

tmp1 = var1.values.flatten()
stats285(tmp1[loc])

05/09/2021 v2.0, Yi Wang

"""
#import matplotlib as mpl
#mpl.use('Agg')
import numpy as np
#import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import xarray as xr

#ds_disk = xr.open_dataset("saved_on_disk.nc")

filename = 'clavrx_MYD021KM.A2019099.1525.061.2019100150615.level2.nc'

fstd = "../dat/clavrx_MYD021KM.A2019099.1525.modis.level2.nc"
frroci =  "../dat/clavrx_MYD021KM.A2019099.1525.rroci.level2.nc"
fnois =  "../dat/clavrx_MYD021KM.A2019099.1525.noise.level2.nc"


with xr.open_dataset(fstd) as dsstd:
#    print(ds_disk.keys())

    print(fstd+' is loaded')
    varstd = dsstd['cld_temp_acha']

with xr.open_dataset(frroci) as dsrroci:
#    print(dsnois.keys())

    print(frroci+' is loaded')
    varrroci = dsrroci['cld_temp_acha']

with xr.open_dataset(fnois) as dsnois:
#    print(dsnois.keys())

    print(fnois+' is loaded')
    varnois = dsnois['cld_temp_acha']

def stats(var):
    a = var.max().values
    b = var.min().values
    c = var.mean().values
    d = var.std().values
    f = (c**2. + d**2.)
    print('max: ',a,'min: ', b,'mean: ', c,'std: ', d, 'uncertainty: ', f)

#print('standard, max, min:',varstd.max(),varstd.min())
print('standard')
stats(varstd)
print('rroci')
stats(varrroci)
print('noise')
stats(varnois)
var1 = varrroci[:] - varstd[:]
var2 = varnois[:] - varstd[:]
var3 = varnois[:] - varrroci[:]

print('rroci - standard')
stats(var1)
print('noise - standard')
stats(var2)
print('noise - rroci')
stats(var3)

#print(np.shape(varrroci))
#print(np.shape(var1))
tmp0 = varrroci.values.flatten()
#tmp2 = var1.values.flatten()
#print(np.shape(tmp1))
#print(np.shape(tmp2))

loc = np.where(tmp0 < 285.)
#print(np.shape(loc))
#print(loc[:10])

def stats285(var):
    a = np.nanmax(var)
    b = np.nanmin(var)
    c = np.nanmean(var)
    d = np.nanstd(var)
    f = (c**2. + d**2.)
    print('max: ',a,'min: ', b,'mean: ', c,'std: ', d, 'uncertainty: ', f)


print('rroci - standard <285')
tmp1 = var1.values.flatten()
stats285(tmp1[loc])
print('noise - standard <285')
tmp2 = var2.values.flatten()
stats285(tmp2[loc])
print('noise - rroci <285')
tmp3 = var3.values.flatten()
stats285(tmp3[loc])


