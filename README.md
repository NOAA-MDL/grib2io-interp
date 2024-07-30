# grib2io-interp: Interpolation Component Package for grib2io

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

![Build Linux](https://github.com/NOAA-MDL/grib2io-interp/actions/workflows/build_linux.yml/badge.svg)

![PyPI](https://img.shields.io/pypi/v/grib2io-interp?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/grib2io-interp)

[![Anaconda-Server Badge](https://anaconda.org/conda-forge/grib2io-interp/badges/version.svg)](https://anaconda.org/conda-forge/grib2io-interp)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/grib2io-interp/badges/platforms.svg)](https://anaconda.org/conda-forge/grib2io-interp)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/grib2io-interp/badges/downloads.svg)](https://anaconda.org/conda-forge/grib2io-interp)

# Introduction
`grib2io-interp` is an interpolation component package for [grib2io](https://github.com/NOAA-MDL/grib2io).  This package provides a Python interface to the [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip) Fortran library via a NumPy/F2PY extension module.  Originally, grib2io-interp was a part of the grib2io package, but since it requires NumPy.distutils to build and install, it needs to be handled separately from the main grib2io source that are using `setuptools`.  This package contains an extension module, `interpolate`, that provides interfaces to Fortran subroutines and these subroutines serve as wrappers to NCEPLIBS-ip subroutines.  The following table illustrates the mapping:

| grib2io-interp | NCEPLIBS-ip |
| -------------- | ----------- |
| interpolate.interpolate_scalar | ipolates_grib2 |
| interpolate.interpolate_vector | ipolatev_grib2 |

**NOTE:** It is recommended that you use [`grib2io.interpolate`](https://noaa-mdl.github.io/grib2io/grib2io.html#interpolate) function to access the interpolation subroutines provided by grib2io-interp.

## Documentation
[NOAA-MDL/grib2io-interp](https://noaa-mdl.github.io/grib2io-interp/grib2io-interp.html)

## Required Software

Despite this package being a component for grib2io, grib2io is not a formal dependency for grib2io-interp.

* [Python](https://python.org) 3.8, 3.9, 3.10, and 3.11
* [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip) 4.1.0+
* [NCEPLIBS-sp](https://github.com/NOAA-EMC/NCEPLIBS-sp) 2.5.0+ _**(IMPORTANT: required if NCEPLIBS-ip < v5.0.0)**_
* setuptools 61.0+
* NumPy 1.22+ _**(NumPy v2.x not supported at this time)**_
* Fortran Compiler: GNU (gfortran) and Intel (ifort) have been tested.

## NCEPLIBS-ip

> [!NOTE]
> Beginning with NCEPLIBS-ip v5.0.0, the NCEP Spectral Interpolation [(NCEPLIBS-sp)](https://github.com/NOAA-EMC/NCEPLIBS-sp) library is now integrated into NCEPLIBS-ip.

> [!NOTE]
> Beginning with NCEPLIBS-ip v5.1.0, you can now interpolate from Rotated Lat/Lon Arakawa B and E Grids (Grid Definition Template numbers 32768 and 32769).

## Installation

### pip
If NCEPLIBS-ip has been installed to custom location (i.e. not default paths), then define the root of the installation via environment variable `IP_DIR`. If the NCEPLIBS-ip version is < 5.0.0, then you will need to install NCEPLIBS-sp and if installed to a custom location, then define the root of the installation via environment variable `SP_DIR`.
```shell
pip install grib2io-interp
```

### conda
All required libraries are available in conda-forge.
```shell
conda install -c conda-forge grib2io-interp
```

## Build and Install from Source

* Clone GitHub repository or download a source release from [GitHub](https://github.com/NOAA-MDL/grib2io-interp) or [PyPI](https://pypi.python.org/pypi/grib2io-interp).

* Edit `setup.cfg` to define the NCEPLIBS-ip library installation path __OR__ define `IP_DIR` environment variable.

* Build and install.  Use `--user` to install into personal space (`$HOME/.local`).

```shell
pip install .
```
To build with Intel compilers, perform the following
```shell
pip install . --config-settings="--build-option=build --fcompiler=intelem"
```

> [!NOTE]
> ### Building with static libraries
> The default behavior for building grib2io-interp is to build against shared-object libraries.  However, in production environments, it is beneficial to build against static library files.  grib2io-interp (v1.2.0+) allows for this type of build configuration.  To build against static library files, set the environment variable, `USE_STATIC_LIBS="True"` before your build/install command.  For example,
> 
>```shell
>export USE_STATIC_LIBS="True"
>pip install . --config-settings="--build-option=build ==fcompiler=gnu95"
>```

## Development

The development evolution of grib2io-interp will mainly focus on how best to serve that purpose and its primary user's -- mainly meteorologists, physical scientists, and software developers supporting the missions within NOAA's National Weather Service (NWS) and National Centers for Environmental Prediction (NCEP), and other NOAA organizations.

## Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an 'as is' basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.
