"""
used for comparing the difference of 2 granules after removing 285K pixels
compare 3 datasets
1) MODIS
2) RROCI
3) RROCI ADDED NOISE

plot histogram with step mode

xarray -> dataarray -> numpy array

05/09/2021 v1.0, Yi Wang

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


def cvrxr2nparray(var):
    tmp = var.values
    tmp = tmp[~np.isnan(tmp)]
    tmp = tmp[tmp<285]
    return tmp


def stats285(var):
    a = np.max(var)
    b = np.min(var)
    c = np.mean(var)
    d = np.std(var)
    f = (c**2. + d**2.)
    print('max: ',a,'min: ', b,'mean: ', c,'std: ', d, 'uncertainty: ', f)

fig, axs = plt.subplots(nrows=3, ncols=2)

array0 = cvrxr2nparray(varstd)
#axs[0, 0].hist(array0, 20, density=True, histtype='step', facecolor='g')
axs[0, 0].hist(array0, 20, histtype='step', edgecolor='grey')
axs[0, 0].set_title('MODIS')
axs[0, 0].set_ylim(0,200000)
axs[0, 0].set_xlim(195,305)

array1 = cvrxr2nparray(varrroci)
axs[1, 0].hist(array1, 20,  histtype='step', edgecolor='grey')
axs[1, 0].set_title('RROCI')
axs[1, 0].set_ylim(0,200000)
axs[1, 0].set_xlim(195,305)

array2 = cvrxr2nparray(varnois)
axs[2, 0].hist(array2, 20,  histtype='step', edgecolor='grey')
axs[2, 0].set_title('NOISE')
axs[2, 0].set_ylim(0,200000)
axs[2, 0].set_xlim(195,305)

array3 = cvrxr2nparray(var1)
axs[0, 1].hist(array3, 20, histtype='step', edgecolor='grey')
axs[0, 1].set_title('RROCI - MODIS')
axs[0, 1].set_ylim(0,1100000)
axs[0, 1].set_xlim(-11,41)

array4 = cvrxr2nparray(var2)
axs[1, 1].hist(array4, 20,  histtype='step', edgecolor='grey')
axs[1, 1].set_title('NOISE - MODIS')
axs[1, 1].set_ylim(0,1100000)
axs[1, 1].set_xlim(-11,41)

array5 = cvrxr2nparray(var3)
axs[2, 1].hist(array5, 20,  histtype='step', edgecolor='grey')
axs[2, 1].set_title('NOISE - RROCI')
axs[2, 1].set_ylim(0,1100000)
axs[2, 1].set_xlim(-11,41)
print('rroci - standard <285')
stats285(array3)
print('noise - standard <285')
stats285(array4)
print('noise - rroci <285')
stats285(array5)


#fig = plt.figure(figsize=(6.1,5))
#ax=fig.add_subplot(321)

fig.tight_layout()

pngname = "../fig/"+"fig_cthdiff285"+".pdf"
print("save ", pngname)
plt.savefig(pngname, dpi=100, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches='tight', pad_inches=0.1)

plt.show()
