"""
Introduction
============

grib2io_interp is a component package to the parent package, [grib2io](https://github.com/NOAA-MDL/grib2io).
This package provides interfaces to the [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip) general
interpolation library.

grib2io_interp provides interfaces for performing scalar and vector interpolation.  `grib2io_interp.interpolate` is
a f2py module extension that contains 2 subroutines: `interpolate_scalar` and `interpolate_vector`.  These
subroutines serve as wrappers to the NCEPLIBS-ip subroutines `ipolates_grib2` and `ipolatev_grib2` respectively.

It is **recommended** that you access these interpolation subroutines via [`grib2io.interpolate()`](https://noaa-mdl.github.io/grib2io/grib2io.html#interpolate).
"""

from .__config__ import grib2io_interp_version as __version__

try:
    from .openmp_handler import *
except(ImportError):
    pass
