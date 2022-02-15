# geogeneral

I tested 4 python packages, not every package read the hdf4/hdf5 data correctly.

package name | xarray | h5py | #riorxarray | pyhdf
--- | --- | --- | --- |--- 
MODIS HDF4 | not | not | correct, but extracted scale/offset values may not correct| correct 
HDF5 | not | correct | correct, but extracted scale/offset values may not correct | not applicable

