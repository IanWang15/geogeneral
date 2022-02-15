path1 = './dat/'
filename1 = path1+'filename.h5'

import rioxarray as rxr

iscale = 0.000274562517166662
iadd = -0.52392

def loaddat(filename,varname):
    ds1 = rxr.open_rasterio(filename, masked=True)
    #    print(ds1.keys())
    var1 = ds1[varname]
    print(var1.add_offset)
    print(var1.scale_factor)

    var1 = (var1 - iadd) * iscale
    varlat = ds1['latitude']
    varlon = ds1['longitude']

    arrlon = np.array(varlon[:,:]).flatten()
    arrlat = np.array(varlat[:,:]).flatten()
    arr0 = np.array(var1[:,:]).flatten()

    lon = arrlon[::1]
    lat = arrlat[::1]
    data = arr0[::1]

    return lat, lon, data

lat, lon, data = loaddat(filename1,'variable_name')

