import numpy as np

path1 = './dat/'
filename1 = 'MYD021KM.A2019099.2040.061.2019100150925.hdf' # channel 8

import rioxarray as rxr

modis_pre = rxr.open_rasterio(path1+filename1, masked=True)
channum = 1 # for rroci
bandloc = 0 # for modis

ctt = modis_pre[0]['EV_250_Aggr1km_RefSB']

print(list(ctt.attrs))

sf=ctt.scale_factor
offset=ctt.add_offset
print('sf, offset', sf, offset)

sf=ctt.radiance_scales
offset=ctt.radiance_offsets
print('sf, offset', sf, offset)


