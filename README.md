# grib2io-interp: Spatial Interpolation component for grib2io

![Build Linux](https://github.com/NOAA-MDL/grib2io-interp/actions/workflows/build_linux.yml/badge.svg)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![PyPI version](https://badge.fury.io/py/grib2io.svg)](https://badge.fury.io/py/grib2io-interp)

# Introduction
`grib2io-interp` is the spatial interpolation component for [grib2io](https://github.com/NOAA-MDL/grib2io).  This package provides a Python interface to the [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip) Fortran Library and contains a single NumPy/F2PY extension module.  Originally, it was a part of the grib2io package, but since it requires NumPy's distutil's `Extension` and `setup` to build and install, it needs to be handled separately from the other grib2io source that are using `setuptools`.

## Documentation
[NOAA-MDL/grib2io-interp](https://noaa-mdl.github.io/grib2io-interp/grib2io-interp.html)

## Required Software
* [Python](https://python.org) 3.8+
* [NCEPLIBS-sp](https://github.com/NOAA-EMC/NCEPLIBS-sp) 2.4.0+
* [NCEPLIBS-ip](https://github.com/NOAA-EMC/NCEPLIBS-ip) 4.1.0+
* [grib2io](https://github.com/NOAA-MDL/grib2io) 2.0.0+
* setuptools
* NumPy 1.22+
* C and Fortran Compiler: GNU, Intel, and Apple Clang have been tested.

## NCEPLIBS Libraries

### sp and ip
The NCEP Spectral Interpolation (NCEPLIBS-sp) library is a dependency for the NCEP Interpolation (NCEPLIBS-ip) library.  Both of these libraries are Fortran-based and contains OpenMP directives.

## Installation
If NCEPLIBS-sp, and NCEPLIBS-ip libraries have been installed to custom locations (i.e. not default paths), then please define the root of these installations via environment variables `SP_DIR`, and `IP_DIR`, respectively.
```shell
pip install grib2io-interp
```

## Build and Install from Source

* Clone GitHub repository or download a source release from [GitHub](https://github.com/NOAA-MDL/grib2io-interp) or [PyPI](https://pypi.python.org/pypi/grib2io-interp).

* Edit `setup.cfg` to define the sp, and ip library installation paths __OR__ define `SP_DIR` and `IP_DIR` environment variables.

* Build and install.  Use `--user` to install into personal space (`$HOME/.local`).

```shell
python setup.py build --fcompiler=[gnu95|intelem] # GNU or Intel compilers
python setup.py install
```
OR
```shell
pip install . --global-option="build" --global-option="--fcompiler=[gnu95|intelem]"
```
