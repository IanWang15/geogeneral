"""
    Name:
       cmpvarcttdayv2.py
    Purpose:
        batch processing with arguments
        The argument determined the difference between cloud top temperature from 2 datasets
        to load everything in a hdf file using the SD
    Calling Sequence:
        e.g.
        python cmpvarcttday.py 20
        the output folder should set up in advance
    Input: 
        FILE_NAME: listl2day.txt, which lists the file names from dataset folder
    Output:
        to write 1 variable in a single file
        output separates into thin and thick clouds
    Keywords: 
       none
    Dependencies:
        numpy
        pyhdf, SDC, SD
    Required files:
        listl2day.txt
    Example:
        ...
    Modification History:
        Written (v1.0): Yi Wang, 06/08/2021, STC
        Written (v2.0): Yi Wang, 06/10/2021, STC
          modify to print more variables in a row
          input file dir changed
        Written (v3.0): Yi Wang, 06/10/2021, STC
          compare RROCI 8 bands with noise
        
"""

#import matplotlib as mpl
#mpl.use('Agg')
import numpy as np
#import matplotlib.pyplot as plt
import xarray as xr
from functools import reduce
import sys

if sys.argv[1]:
    diffrange = sys.argv[1]
else:
    print('no input different range, using default value str(25)')
    diffrange = 25

diffrange = int(diffrange)

#ds_disk = xr.open_dataset("saved_on_disk.nc")
#dirstd = '/mnt/efs_clavrx/clavrx/golden_day_20190409/level2/CLAVRx_3_0/day/MODIS_baseline/'
#dirnois = '/mnt/efs_clavrx/ywang/run/06022021/nois_day/output/'

dirstd = '/mnt/efs_clavrx/sharedata/RROCI_baseline/day/'
dirnois = '/mnt/efs_clavrx/sharedata/RROCI_allBandsNoised/day/'

with open('./listl2day.txt') as f:
    content = f.readlines()

for i in range(len(content)):
    timeidx = content[i][:-1][-32:-28]

#    fstdi = 'clavrx_a1.19099.'+timeidx+'.1000m.level2.nc'

    fstd = dirstd + content[i][:-1]#fstdi
    fnois = dirnois + content[i][:-1]
    print(content[i][:-1]+' ...')
    with xr.open_dataset(fstd) as dsstd:
#        print(ds_disk.keys())
        varstd = dsstd['cld_temp_acha']
        vartau = dsstd['cld_opd_dcomp']
        varcm  = dsstd['cloud_mask']
        varlat  = dsstd['latitude']
        varlon  = dsstd['longitude']
        varland  = dsstd['land_class']
        varsnow  = dsstd['snow_class']
        varctype  = dsstd['cloud_type']
        varsza  = dsstd['solar_zenith_angle']

    with xr.open_dataset(fnois) as dsnois:
        varnois = dsnois['cld_temp_acha']

    vardiff = varnois[:] - varstd[:]

    varfdiff = vardiff.values.flatten()
    varfstd = varstd.values.flatten()
    varfnois = varnois.values.flatten()
    tmp0 = varcm.values.flatten()
    tmp1 = vartau.values.flatten()
    tmp2 = abs(varfdiff)

    varflat = varlat.values.flatten()
    varflon = varlon.values.flatten()
    varfland = varland.values.flatten()
    varfsnow = varsnow.values.flatten()
    varfctype = varctype.values.flatten()
    varfsza = varsza.values.flatten()

    loc0 = np.where(tmp0 > 1.) # cloud mask = 2 & 3 treat as clouds
    loc1 = np.where(tmp1 < 1.) # thin clouds tau < 1
    loc2 = np.where(tmp1 > 1.) # thick clouds tau > 1
    loc3 = np.where(tmp1 < 164.)
    loc4 = np.where(varfstd < 300.)
    loc5 = np.where(varfstd > 190.)
    loc6 = np.where(tmp2 < diffrange)

    locthin = reduce(np.intersect1d, (loc0, loc1, loc3, loc4, loc5, loc6))
    cldthin = varfdiff[locthin]
#    cldthin = cldthin[~np.isnan(cldthin)]
#    np.savetxt('/mnt/efs_clavrx/ywang/run/06082021/dat/'+str(diffrange)+'/day/thin/'+timeidx+'.txt',cldthin)
    prt0 = varflat[locthin]
    prt1 = varflon[locthin]
    prt2 = cldthin
    prt3 = tmp1[locthin]
    prt4 = varfland[locthin]
    prt5 = varfsnow[locthin]
    prt6 = varfctype[locthin]
    prt7 = varfsza[locthin]
    prt8 = varfstd[locthin]
    prt9 = varfnois[locthin]

    f0=open('/mnt/efs_clavrx/ywang/run/06082021/dat/geospl8b/'+str(diffrange)+'/day/thin/'+timeidx+'.txt','w')

    f0.write('# lat   lon   ctt   tau   landFlg   snowFlg   cldType   sza  CTTstd  CTTnois \n')
    for i in range(len(prt2)):
        f0.write(str(prt0[i])+' '+str(prt1[i])+' '+str(prt2[i])+' '+str(prt3[i])+' '+str(prt4[i])+' '\
            +str(prt5[i])+' '+str(prt6[i])+' '+str(prt7[i])+' '+str(prt8[i])+' '+str(prt9[i])+'\n')
    f0.close()

    locthick = reduce(np.intersect1d, (loc0, loc2, loc3, loc4, loc5, loc6))
    cldthick = varfdiff[locthick]
#    cldthick = cldthick[~np.isnan(cldthick)]

    prt0 = varflat[locthick]
    prt1 = varflon[locthick]
    prt2 = cldthick
    prt3 = tmp1[locthick]
    prt4 = varfland[locthick]
    prt5 = varfsnow[locthick]
    prt6 = varfctype[locthick]
    prt7 = varfsza[locthick]
    prt8 = varfstd[locthick]
    prt9 = varfnois[locthick]

    f0=open('/mnt/efs_clavrx/ywang/run/06082021/dat/geospl8b/'+str(diffrange)+'/day/thick/'+timeidx+'.txt','w')

    f0.write('# lat   lon   ctt   tau   landFlg   snowFlg   cldType   sza  CTTstd  CTTnois \n')
    for i in range(len(prt2)):
        f0.write(str(prt0[i])+' '+str(prt1[i])+' '+str(prt2[i])+' '+str(prt3[i])+' '+str(prt4[i])+' '\
            +str(prt5[i])+' '+str(prt6[i])+' '+str(prt7[i])+' '+str(prt8[i])+' '+str(prt9[i])+'\n')
    f0.close()

#    np.savetxt('/mnt/efs_clavrx/ywang/run/06082021/dat/geospl/'+str(diffrange)+'/day/thick/'+timeidx+'.txt',cldthick)

#tmp2 = abs(var)
#print(np.shape(np.where(tmp0 == 0.)))

#import pdb 
#pdb.set_trace() 
#print('stop here')
print('computation is finished')
