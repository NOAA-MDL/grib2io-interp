"""
Introduction
============

grib2io_interp is a component package to the parent package, [grib2io](https://github.com/NOAA-MDL/grib2io).
This package provides interfaces to the Fortran-based [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip)
general interpolation library. The interface supports performing scalar and vector interpolation. `grib2io_interp.interpolate`
is a F2PY extension module that contains 2 subroutines: `interpolate_scalar` and `interpolate_vector`.  These
subroutines serve as wrappers to the NCEPLIBS-ip subroutines `ipolates_grib2` and `ipolatev_grib2` respectively.

It is **recommended** that you access these interpolation subroutines via [`grib2io.interpolate()`](https://noaa-mdl.github.io/grib2io/grib2io.html#interpolate).

OpenMP Support
==============

NCEPLIBS-ip can be built with support for OpenMP threading. This is also supported in grib2io-interp. The
F2PY signatures for `interpolate_scalar` and `interpolate_vector` subroutines contain the keyword `threadsafe`
which unlocks Python's global interpretor lock (gil) and allows for threading. grib2io-interp contains a
second F2PY extension module, `grib2io_interp.openmp_handler`, that allows the user to get and set the number
of OpenMP threads.  These functions are made public by `grib2io_interp.get_openmp_threads()` and 
`grib2io_interp.set_openmp_threads()`.
"""

from .__config__ import grib2io_interp_version as __version__
from .__config__ import has_openmp_support

def get_openmp_threads():
    """
    Return the number of OpenMP threads.

    Returns
    -------
    int
        The number of OpenMP threads.
    """
    try:
        from . import openmp_handler
        return openmp_handler.get_openmp_threads()
    except(ImportError):
        pass

def set_openmp_threads(n: int):
    """
    Set the number of OpenMP threads.

    Parameters
    ----------
    n
        The number of OpenMP threads.
    """
    if n < 1:
        raise ValueError(f'Number of threads must be > 0.')
    try:
        from . import openmp_handler
        openmp_handler.set_openmp_threads(n)
    except(ImportError):
        pass
