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
import matplotlib.pyplot as plt
from matplotlib import colorbar, colors
import xarray as xr

fstd = "../dat/clavrx_MYD021KM.A2019099.1525.modis.level2.nc"
faer =  "../dat/clavrx_a1.19099.1525.1000m_allBandsNoised.level2aer.nc"
fnois =  "../dat/clavrx_MYD021KM.A2019099.1525.noise.level2.nc"
frroci = "../dat/clavrx_a1.19099.1525.1000m_RROCI_baseline.level2.nc"

with xr.open_dataset(fstd, mask_and_scale = True) as dsstd:
#    print(dsnois.keys())
    print(fstd+' is loaded')
    varstd = dsstd['cld_temp_acha']
    lat = dsstd['latitude']
    lon = dsstd['longitude']

with xr.open_dataset(faer, mask_and_scale = True) as dsaer:
#    print(dsnois.keys())
    print(faer+' is loaded')
    varaer = dsaer['cld_temp_acha']
#    varcfaer = dsaer['cloud_mask']

with xr.open_dataset(frroci, mask_and_scale = True) as dsrroci:
#    print(dsnois.keys())
    print(frroci+' is loaded')
    varrroci = dsrroci['cld_temp_acha']

with xr.open_dataset(fnois, mask_and_scale = True) as dsnois:
#    print(dsnois.keys())
    print(fnois+' is loaded')
    varnois = dsnois['cld_temp_acha']
    varcf = dsnois['cloud_mask']

fmodis = '../dat/MYD021KM.A2019099.1525.061.2019100150615.hdf'

with xr.open_dataset(fmodis) as dsmodis:
#    print(dsnois.keys())
    print(fmodis+' is loaded')
    dsmodis500 = dsmodis['EV_500_Aggr1km_RefSB']
#idxcf = dscf.values.flatten()
#loc = np.where(idxcf == 3.)
varmds = ((dsmodis500.values)[3,:,:] * 0.0027294294)
idxmds = varmds.flatten()
idxcf = varcf.values.flatten()

varnoisstd = (varnois[:] - varstd[:]).values.flatten()
varrrocistd = (varrroci[:] - varstd[:]).values.flatten()
varnoisaer = (varnois[:] - varaer[:]).values.flatten()
varnoisrroci = (varnois[:] - varrroci[:]).values.flatten()
varaerstd = (varaer[:] - varstd[:]).values.flatten()

import cartopy.crs as ccrs

fig = plt.figure(figsize=(6, 6))

#data = varrrocistd[(idxcf == 3.) & (idxmds < 100.)]
#data = varnoisstd[(idxcf == 3.) & (idxmds < 100.)]
#data = varnoisrroci[(idxcf == 3.) & (idxmds < 100.)]
data = varnoisaer[(idxcf == 3.) & (idxmds < 100.)]

lon = lon.values.flatten()[(idxcf == 3.) & (idxmds < 100.)]
lat = lat.values.flatten()[(idxcf == 3.) & (idxmds < 100.)]

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-60, 0, -50, -10], crs=ccrs.PlateCarree())

mm = ax.scatter(lon[::100], lat[::100], c=data[::100],cmap='rainbow',s=1.2, vmin=0, vmax=10)
ax.coastlines()
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
#ax.set_title('Cloud Top Temperature (K)')

cbar_ax = fig.add_axes([1.05, 0.25, 0.03, 0.5])
#cbar_ax.set_label('Cloud Top Temperature (K)')

cbar = plt.colorbar(mm, cax=cbar_ax)

#cbar.set_clim(0., 10.) # set limits of color map

fig.tight_layout()

pngname = "../fig/"+"fig_glob8"+".pdf"
print("save ", pngname)
plt.savefig(pngname, dpi=100, facecolor='w', edgecolor='w',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches='tight', pad_inches=0.1)

plt.show()

