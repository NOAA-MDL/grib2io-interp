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

NCEP Grid Template 32769
========================

[NCEPLIBS-ip v5.1.0](https://github.com/NOAA-EMC/NCEPLIBS-ip/releases/tag/v5.1.0) allows for interpolation
from Rotated Latitude/Longitude Arakawa Grids, specifically grid templates [32768](https://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp3-32768.shtml)
and [32769](https://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_doc/grib2_temp3-32769.shtml). In order to interpolate
from this grid, the `ncep_post_arakawa` logical scalar in the ip::ip_grid_mod needs to be set to `.true.`. In grib2io_interp,
we have an interface to set this flag with `grib2io_interp.set_ncep_post_arakawa_flag()`. Note that is is only
necessary for template 32769.
"""

from .__config__ import grib2io_interp_version as __version__
from .__config__ import has_openmp_support

def set_ncep_post_arakawa_flag(flag: bool):
    """
    Set the value of the ncep_post_arakawa logical scalar from
    ip::ip_grid_mod.

    Parameters
    ----------
    flag
        Set to `True` or `False` to use the NCEP post method for
        Arakawa grids.
    """
    try:
        from . import interpolate
        interpolate.set_ncep_post_arakawa_flag(flag)
    except(AttributeError):
        raise AttributeError(f"""

set_ncep_post_arakawa_flag() is available when grib2io-interp
has been built with NCEPLIBS-ip v5.1.0+.

""")
    except(ImportError):
        pass

def get_ncep_post_arakawa_flag():
    """
    Get the value of the ncep_post_arakawa logical scalar from
    ip::ip_grid_mod.

    Returns
    -------
    bool
    """
    try:
        from . import interpolate
        value = interpolate.get_ncep_post_arakawa_flag()
        return True if value == 1 else False
    except(AttributeError):
        raise AttributeError(f"""

get_ncep_post_arakawa_flag() is available when grib2io-interp
has been built with NCEPLIBS-ip v5.1.0+.

""")
    except(ImportError):
        pass

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
