import numpy as np
from pyhdf.SD import SD,SDC

def statsnp(var):
    a = np.nanmax(var)
    b = np.nanmin(var)
    c = np.nanmedian(var)
    d = np.nanstd(var)
    e = np.nanmean(var)
    f = (c**2. + d**2.)
    print('max: ',a,'min: ', b,'median: ', c,'std: ', d, 'mean: ', e, 'uncertainty: ', f)

file00 = 'MYD021KM.A2019099.2040.061.2019100150925.hdf'

dfdir = './dat/'+file00
#hf00 = SD(dfdir,SDC.WRITE)
hf00 = SD(dfdir,SDC.READ)
datasets_dic = hf00.datasets()

def readvar(varname):
    i00_obj = hf00.select(varname)
    i00 = i00_obj.get()

    add_offset,scale_factor = 0., 0.
    for key, value in i00_obj.attributes().items():
        if key == 'radiance_offsets':#,'add_offset':
            add_offset = value
        if key == 'radiance_scales':#,'scale_factor':
            scale_factor = value

    varfillvalue = i00_obj.getfillvalue()
    i00_obj.endaccess()

    return i00,add_offset,scale_factor,varfillvalue

def writevar(varname, var):
    i01_obj = hf00.select(varname)
    i01 = i01_obj.get()
    i01_obj.set(var)
    i01_obj.endaccess()

# read variable
var250,addfst250,sclfct250,vrfll250 = readvar('EV_250_Aggr1km_RefSB')

statsnp(var250)

varw1 = np.zeros(shape = (np.shape(var250)[0],np.shape(var250)[1],np.shape(var250)[2]))
varw1[:,:,:] = varw1

# write into the file
#writevar('EV_250_Aggr1km_RefSB',varw1)

