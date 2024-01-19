# fmt: off
from numpy.distutils.core import Extension, setup
import configparser
from ctypes.util import find_library as ctypes_find_library
import numpy
import os
from pathlib import Path
import sys

VERSION = '1.0.3'

libdirs = []
incdirs = []
libraries = ['sp_4','ip_4']
if sys.platform == "win32":
    libraries = ["sp_4", "ip_4"]


# fmt: on
# ----------------------------------------------------------------------------------------
# find_library.
# ----------------------------------------------------------------------------------------
def find_library(name, dirs=None):
    _libext_by_platform = {"linux": ".so", "darwin": ".dylib", "win32": ".dll"}
    out = []
    sysinfo = (os.name, sys.platform)

    # According to the ctypes documentation Mac and Windows ctypes_find_library
    # returns the full path.  Also ctypes_find_library returns None for macOS
    # on Apple Silicon.
    if sys.platform != "linux":
        for sname in [ctypes_find_library(name), ctypes_find_library(f"lib{name}")]:
            if sname is not None:
                return sname

    # For Linux and macOS on Apple Silicon have to search ourselves.
    libext = _libext_by_platform[sys.platform]

    if dirs is None:
        dirs = []
        if os.environ.get("CONDA_PREFIX"):
            dirs.extend([os.environ["CONDA_PREFIX"]])
        if os.environ.get("LD_LIBRARY_PATH"):
            dirs.extend(os.environ.get("LD_LIBRARY_PATH").split(":"))
        dirs.extend(
            ["/usr/local", "/sw", "/opt", "/opt/local", "/opt/homebrew", "/usr"]
        )

    out = []
    for d in dirs:
        libs = Path(d).rglob(f"lib{name}{libext}")
        out.extend(libs)
        if out:
            break
    if not out:
        raise ValueError(
            f"""

The library "{name}{libext}" could not be found in any of the following
directories:
{dirs}

"""
        )
    return out[0].absolute().resolve().as_posix()


# fmt: off


# ----------------------------------------------------------------------------------------
# Read setup.cfg
# ----------------------------------------------------------------------------------------
setup_cfg = 'setup.cfg'
config = configparser.ConfigParser()
config.read(setup_cfg)

# ----------------------------------------------------------------------------------------
# Get NCEPLIBS-sp library info.  NOTE: NCEPLIBS-sp does not have include files.
# ----------------------------------------------------------------------------------------
if os.environ.get('SP_DIR'):
    sp_dir = os.environ.get('SP_DIR')
    sp_libdir = os.path.dirname(find_library('sp_4', dirs=[sp_dir]))
else:
    sp_dir = config.get('directories','sp_dir',fallback=None)
    if sp_dir is None:
        sp_libdir = os.path.dirname(find_library('sp_4'))
    else:
        sp_libdir = os.path.dirname(find_library('sp_4', dirs=[sp_dir]))
libdirs.append(sp_libdir)

# ----------------------------------------------------------------------------------------
# Get NCEPLIBS-ip library info.
# ----------------------------------------------------------------------------------------
if os.environ.get('IP_DIR'):
    ip_dir = os.environ.get('IP_DIR')
    ip_libdir = os.path.dirname(find_library('ip_4', dirs=[ip_dir]))
    ip_incdir = os.path.join(ip_dir,'include_4')
else:
    ip_dir = config.get('directories','ip_dir',fallback=None)
    if ip_dir is None:
        ip_libdir = os.path.dirname(find_library('ip_4'))
        ip_incdir = os.path.join(os.path.dirname(ip_libdir),'include_4')
    else:
        ip_libdir = os.path.dirname(find_library('ip_4', dirs=[ip_dir]))
        ip_incdir = os.path.join(os.path.dirname(ip_libdir),'include_4')
libdirs.append(ip_libdir)
incdirs.append(ip_incdir)

libdirs = list(set(libdirs))
incdirs = list(set(incdirs))
incdirs.append(numpy.get_include())

# Weird change in how Windows looks for DLLs.  Used to follow system PATH
# environment variable but changed to having to explicitly set for security
# reasons.
if "add_dll_directory" in dir(os):
    for ldir in libdirs:
        os.add_dll_directory(ldir)

# ----------------------------------------------------------------------------------------
# Define interpolation NumPy extension module.
# ----------------------------------------------------------------------------------------
interpext = Extension(name = 'grib2io_interp.interpolate',
                      sources = ['src/interpolate/interpolate.pyf','src/interpolate/interpolate.f90'],
                      extra_f77_compile_args = ['-O3','-fopenmp'],
                      extra_f90_compile_args = ['-O3','-fopenmp'],
                      include_dirs = incdirs,
                      library_dirs = libdirs,
                      runtime_library_dirs = libdirs,
                      libraries = libraries)

# ----------------------------------------------------------------------------------------
# Create __config__.py
# ----------------------------------------------------------------------------------------
cnt = \
"""# This file is generated by grib2io-interps's setup.py
# It contains configuration information when building this package.
grib2io_interp_version = '%(grib2io_interp_version)s'
"""
a = open('src/grib2io_interp/__config__.py','w')
cfgdict = {}
cfgdict['grib2io_interp_version'] = VERSION
try:
    a.write(cnt % cfgdict)
finally:
    a.close()

# ----------------------------------------------------------------------------------------
# Import README.md as PyPi long_description
# ----------------------------------------------------------------------------------------
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# ----------------------------------------------------------------------------------------
# Run setup
# ----------------------------------------------------------------------------------------
setup(ext_modules       = [interpext],
      long_description  = long_description,
      long_description_content_type = 'text/markdown')
