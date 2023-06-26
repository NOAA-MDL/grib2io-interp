import pytest
import numpy as np
import datetime
import grib2io

# Grid specs to interp to (NBM CONUS 5KM)
gdtn_nbm = 30
gdt_nbm = [1, 0, 6371200, 255, 255, 255, 255, 1173, 799, 19229000, 233723400,
           48, 25000000, 265000000, 5079406, 5079406, 0, 64, 25000000,
           25000000, -90000000, 0]

nbm_grid_def = grib2io.Grib2GridDef(gdtn_nbm, gdt_nbm)
nx = gdt_nbm[7]
ny = gdt_nbm[8]

rtol = 1e-04

def _writer(path,a):
    """
    """
    fd = open(path,"wb")
    fd.write(np.ravel(a).tobytes())
    fd.close()

def test_bicubic_interp_to_grid(request):
    data = request.config.rootdir / 'tests' / 'input_data'
    outputdata = request.config.rootdir / 'tests' / 'output_data'
    filename = 'bicubic-interp-grid-output.bin'
    with grib2io.open(data / 'gfs.t00z.pgrb2.1p00.f024') as f:
        msg = f.select(shortName='TMP',level='2 m above ground')[0]
        newmsg = msg.interpolate('bicubic',nbm_grid_def)
        #_writer(outputdata / filename,newmsg.data)
        x = newmsg.data
        y = np.fromfile(outputdata / filename,dtype=np.float32).reshape(ny,nx)
        np.testing.assert_allclose(x,y,rtol=rtol)

def test_bilinear_interp_to_grid(request):
    data = request.config.rootdir / 'tests' / 'input_data'
    outputdata = request.config.rootdir / 'tests' / 'output_data'
    filename = 'bilinear-interp-grid-output.bin'
    with grib2io.open(data / 'gfs.t00z.pgrb2.1p00.f024') as f:
        msg = f.select(shortName='TMP',level='2 m above ground')[0]
        newmsg = msg.interpolate('bilinear',nbm_grid_def)
        #_writer(outputdata / filename,newmsg.data)
        x = newmsg.data
        y = np.fromfile(outputdata / filename,dtype=np.float32).reshape(ny,nx)
        np.testing.assert_allclose(x,y,rtol=rtol)

def test_budget_interp_to_grid(request):
    data = request.config.rootdir / 'tests' / 'input_data'
    outputdata = request.config.rootdir / 'tests' / 'output_data'
    filename = 'budget-interp-grid-output.bin'
    with grib2io.open(data / 'gfs.t00z.pgrb2.1p00.f024') as f:
        msg = f.select(shortName='TMP',level='2 m above ground')[0]
        newmsg = msg.interpolate('budget',nbm_grid_def)
        x = newmsg.data
        y = np.fromfile(outputdata / filename,dtype=np.float32).reshape(ny,nx)
        np.testing.assert_allclose(x,y,rtol=rtol)

def test_neighbor_interp_to_grid(request):
    data = request.config.rootdir / 'tests' / 'input_data'
    outputdata = request.config.rootdir / 'tests' / 'output_data'
    filename = 'neighbor-interp-grid-output.bin'
    with grib2io.open(data / 'gfs.t00z.pgrb2.1p00.f024') as f:
        msg = f.select(shortName='TMP',level='2 m above ground')[0]
        newmsg = msg.interpolate('neighbor',nbm_grid_def)
        #_writer(outputdata / filename,newmsg.data)
        x = newmsg.data
        y = np.fromfile(outputdata / filename,dtype=np.float32).reshape(ny,nx)
        np.testing.assert_allclose(x,y,rtol=rtol)

def test_neighbor_budget_interp_to_grid(request):
    data = request.config.rootdir / 'tests' / 'input_data'
    outputdata = request.config.rootdir / 'tests' / 'output_data'
    filename = 'neighbor-budget-interp-grid-output.bin'
    with grib2io.open(data / 'gfs.t00z.pgrb2.1p00.f024') as f:
        msg = f.select(shortName='TMP',level='2 m above ground')[0]
        newmsg = msg.interpolate('neighbor-budget',nbm_grid_def)
        #_writer(outputdata / filename,newmsg.data)
        x = newmsg.data
        y = np.fromfile(outputdata / filename,dtype=np.float32).reshape(ny,nx)
        np.testing.assert_allclose(x,y,rtol=rtol)
