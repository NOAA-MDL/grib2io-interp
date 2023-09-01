# grib2io-interp: Spatial Interpolation component for grib2io

![Build Linux](https://github.com/NOAA-MDL/grib2io-interp/actions/workflows/build_linux.yml/badge.svg)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![PyPI version](https://badge.fury.io/py/grib2io-interp.svg)](https://badge.fury.io/py/grib2io-interp)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/grib2io-interp/badges/version.svg)](https://anaconda.org/conda-forge/grib2io-interp)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/grib2io-interp/badges/platforms.svg)](https://anaconda.org/conda-forge/grib2io-interp)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/grib2io-interp/badges/license.svg)](https://anaconda.org/conda-forge/grib2io-interp)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/grib2io-interp/badges/downloads.svg)](https://anaconda.org/conda-forge/grib2io-interp)

# Introduction
`grib2io-interp` is the spatial interpolation component for [grib2io](https://github.com/NOAA-MDL/grib2io).  This package provides a Python interface to the [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip) Fortran Library and contains a single NumPy/F2PY extension module.  Originally, it was a part of the grib2io package, but since it requires NumPy's distutil's `Extension` and `setup` to build and install, it needs to be handled separately from the other grib2io source that are using `setuptools`.  This package contains an extension module, `interpolate`, that provides interfaces to Fortran subroutines and these subroutines serve as wrappers to NCEPLIBS-ip subroutines.  The following table illustrates the mapping:

| grib2io-interp | NCEPLIBS-ip |
| -------------- | ----------- |
| interpolate.interpolate_scalar | ipolates_grib2 |
| interpolate.interpolate_vector | ipolatev_grib2 |

**NOTE:** It is recommended that you use [`grib2io.interpolate`](https://noaa-mdl.github.io/grib2io/grib2io.html#interpolate) function to access the interpolation subroutines provided by grib2io-interp.

## Documentation
[NOAA-MDL/grib2io-interp](https://noaa-mdl.github.io/grib2io-interp/grib2io-interp.html)

## Required Software

Despite this package being a component for grib2io, grib2io is not a formal dependency for grib2io-interp.

* [Python](https://python.org) 3.8+
* [NCEPLIBS-sp](https://github.com/NOAA-EMC/NCEPLIBS-sp) 2.4.0+
* [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip) 4.1.0+
* setuptools 61.0+
* NumPy 1.22+
* Fortran Compiler: GNU (gfortran) and Intel (ifort) have been tested.

## NCEPLIBS Libraries

### sp and ip
The NCEP Spectral Interpolation [(NCEPLIBS-sp)](https://github.com/NOAA-EMC/NCEPLIBS-sp) library is a dependency for the NCEP Interpolation [(NCEPLIBS-ip)](https://github.om/NOAA-EMC/NCEPLIBS-ip) library.  Both of these libraries are Fortran-based and contains OpenMP directives.

## Installation
If NCEPLIBS-sp, and NCEPLIBS-ip libraries have been installed to custom locations (i.e. not default paths), then define the root of these installations via environment variables `SP_DIR`, and `IP_DIR`, respectively.
```shell
pip install grib2io-interp
```

## Build and Install from Source

* Clone GitHub repository or download a source release from [GitHub](https://github.com/NOAA-MDL/grib2io-interp) or [PyPI](https://pypi.python.org/pypi/grib2io-interp).

* Edit `setup.cfg` to define the sp, and ip library installation paths __OR__ define `SP_DIR` and `IP_DIR` environment variables.

* Build and install.  Use `--user` to install into personal space (`$HOME/.local`).

```shell
pip install .
```
To build with Intel compilers, perform the following
```shell
pip install . --config-settings="--build-option=build --fcompiler=intelem"
```

## Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an 'as is' basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.
