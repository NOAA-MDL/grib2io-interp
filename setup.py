from ctypes.util import find_library as ctypes_find_library
from numpy.distutils.core import Extension, setup
from pathlib import Path
import configparser
import numpy
import os
import platform
import subprocess
import sys

def get_version():
    """Get version string"""
    with open("VERSION","rt") as f:
        ver = f.readline().strip()
    return ver

def find_library(name, dirs=None, static=False):
    """Find library"""
    _libext_by_platform = {"linux": ".so", "darwin": ".dylib", "win32": ".dll"}
    out = []

    # According to the ctypes documentation Mac and Windows ctypes_find_library
    # returns the full path.
    if (os.name, sys.platform) != ("posix", "linux"):
        out.append(ctypes_find_library(name))

    # For Linux and macOS (Apple Silicon), we have to search ourselves.
    libext = _libext_by_platform[sys.platform]
    libext = ".a" if static else libext
    if dirs is None:
        if 'CONDA_PREFIX' in os.environ:
            dirs = [os.environ["CONDA_PREFIX"]]
        else:
            dirs = ["/usr/local", "/sw", "/opt", "/opt/local", "/opt/homebrew", "/usr"]
    if os.environ.get("LD_LIBRARY_PATH"):
        dirs = dirs + os.environ.get("LD_LIBRARY_PATH").split(":")

    out = []
    for d in dirs:
        libs = Path(d).rglob(f"lib*{name}{libext}")
        out.extend(libs)
    if not out:
        raise ValueError(f"""

The library "lib{name}{libext}" could not be found in any of the following
directories:
{dirs}

""")
    return out[0].absolute().resolve().as_posix()

def run_ar_command(filename):
    """Run the ar command"""
    cmd = subprocess.run(['ar','-t',filename],
                         stdout=subprocess.PIPE)
    cmdout = cmd.stdout.decode('utf-8')
    return cmdout

def run_nm_command(filename):
    """Run the nm command"""
    cmd = subprocess.run(['nm','-C',filename],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.DEVNULL)
    cmdout = cmd.stdout.decode('utf-8')
    return cmdout

def run_ldd_command(filename):
    """Run the ldd command"""
    cmd = subprocess.run(['ldd',filename],
                         stdout=subprocess.PIPE)
    cmdout = cmd.stdout.decode('utf-8')
    return cmdout

def run_otool_command(filename):
    """Run the otool command"""
    cmd = subprocess.run(['otool','-L',filename],
                         stdout=subprocess.PIPE)
    cmdout = cmd.stdout.decode('utf-8')
    return cmdout

def check_for_openmp(ip_lib, static_lib=False):
    """Check for OpenMP"""
    check = False
    info = ""
    libname = ""
    if static_lib:
        if sys.platform in {'darwin','linux'}:
            info = run_nm_command(ip_lib)
            if 'GOMP' in info:
                check = True
                libname = 'gomp'
            elif 'kmpc' in info:
                check = True
                libname = 'iomp5'
    else:
        if sys.platform == 'darwin':
            info = run_otool_command(ip_lib)
        elif sys.platform == 'linux':
            info = run_ldd_command(ip_lib)
            if 'gomp' in info:
                check = True
                libname = 'gomp'
            elif 'iomp5' in info:
                check = True
                libname = 'iomp5'
            elif 'omp' in info:
                check = True
                libname = 'omp'
    return check, libname

def check_for_sp(ip_lib, static_lib=False):
    """Check for NCEPLIBS-sp"""
    check = False
    info = ""
    if static_lib:
        if sys.platform in {'darwin','linux'}:
            info = run_ar_command(ip_lib)
            if 'splat' not in info and \
               'sp_mod' not in info: check = True
    else:
        if sys.platform == 'darwin':
            info = run_otool_command(ip_lib)
        elif sys.platform == 'linux':
            info = run_ldd_command(ip_lib)
        if 'libsp_4' in info: check=True
    return check 
         
# ----------------------------------------------------------------------------------------
# Main part of script
# ----------------------------------------------------------------------------------------
VERSION = get_version()

needs_sp = False
needs_openmp = False
openmp_libname = ''
use_static_libs = False
libraries = ['ip_4']

incdirs = []
libdirs = []
extra_objects = []
ext_modules = []

# ----------------------------------------------------------------------------------------
# Read setup.cfg
# ----------------------------------------------------------------------------------------
setup_cfg = 'setup.cfg'
config = configparser.ConfigParser()
config.read(setup_cfg)

# ----------------------------------------------------------------------------------------
# Check if static library linking is preferred.
# ----------------------------------------------------------------------------------------
if os.environ.get('USE_STATIC_LIBS'):
    val = os.environ.get('USE_STATIC_LIBS')
    if val not in {'True','False'}:
        raise ValueError('Environment variable USE_STATIC_LIBS must be \'True\' or \'False\'')
    use_static_libs = True if val == 'True' else False
use_static_libs = config.get('options', 'use_static_libs', fallback=use_static_libs)

# ----------------------------------------------------------------------------------------
# Get NCEPLIBS-ip library info.
# ----------------------------------------------------------------------------------------
if os.environ.get('IP_DIR'):
    ip_dir = os.environ.get('IP_DIR')
    ip_libdir = os.path.dirname(find_library('ip_4', dirs=[ip_dir], static=use_static_libs))
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

# ----------------------------------------------------------------------------------------
# Check for if sp and OpenMP library objects are in the ip library
# ----------------------------------------------------------------------------------------
ip_staticlib = find_library('ip_4', dirs=libdirs, static=use_static_libs)
if use_static_libs:
    extra_objects.append(ip_staticlib)
    needs_sp = check_for_sp(ip_staticlib)
    needs_openmp, openmp_libname = check_for_openmp(ip_staticlib)
else:
    iplib = find_library('ip_4', dirs=libdirs, static=use_static_libs)
    needs_sp = check_for_sp(iplib)
    needs_openmp, openmp_libname = check_for_openmp(iplib)

# ----------------------------------------------------------------------------------------
# Get NCEPLIBS-sp library info if needed.
#
# NOTE: This library does not have include files.
# ----------------------------------------------------------------------------------------
if needs_sp:
    if os.environ.get('SP_DIR'):
        sp_dir = os.environ.get('SP_DIR')
        sp_libdir = os.path.dirname(find_library('sp_4', dirs=[sp_dir], static=use_static_libs))
    else:
        sp_dir = config.get('directories','sp_dir',fallback=None)
        if sp_dir is None:
            sp_libdir = os.path.dirname(find_library('sp_4', static=use_static_libs))
        else:
            sp_libdir = os.path.dirname(find_library('sp_4', dirs=[sp_dir], static=use_static_libs))
    libdirs.append(sp_libdir)
    if use_static_libs:
        extra_objects.append(find_library('sp_4', dirs=[sp_libdir], static=use_static_libs))
    libraries.append('sp_4')

libraries = [] if use_static_libs else list(set(libraries))
incdirs = list(set(incdirs))
incdirs.append(numpy.get_include())
libdirs = [] if use_static_libs else list(set(libdirs))
extra_objects = list(set(extra_objects)) if use_static_libs else []

# ----------------------------------------------------------------------------------------
# Get OpenMP library info if needed. Regardless of static or dynamic linking to
# NCEPLIBS-ip (and sp if needed), add the OpenMP library name to libraries to dynamically
# link to.
#
# NOTE: In the future, we might want to allow the user to control either static or dynamic
# linking to the OpenMP library.
# ----------------------------------------------------------------------------------------
if needs_openmp:
    libraries.append(openmp_libname)

print(f'Use static libs: {use_static_libs}')
print(f'Needs OpenMP: {needs_openmp}')
print(f'Needs NCEPLIBS-sp: {needs_sp}')
print(f'\t{libraries = }')
print(f'\t{incdirs = }')
print(f'\t{libdirs = }')
print(f'\t{extra_objects = }')

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
                      libraries = libraries,
                      extra_objects = extra_objects)
ext_modules.append(interpext)

if needs_openmp:
    ompext = Extension(name = 'grib2io_interp.openmp_handler',
                       sources = ['src/openmp_handler/openmp_handler.pyf',
                                  'src/openmp_handler/openmp_handler.f90'],
                       extra_f77_compile_args = ['-O3','-fopenmp'],
                       extra_f90_compile_args = ['-O3','-fopenmp'],
                       include_dirs = incdirs,
                       library_dirs = libdirs,
                       runtime_library_dirs = libdirs,
                       libraries = libraries,
                       extra_objects = extra_objects)
    ext_modules.append(ompext)

# ----------------------------------------------------------------------------------------
# Create __config__.py
# ----------------------------------------------------------------------------------------
cnt = \
"""# This file is generated by grib2io-interps's setup.py
# It contains configuration information when building this package.
grib2io_interp_version = '%(grib2io_interp_version)s'
has_openmp_support = %(has_openmp_support)s
"""
a = open('src/grib2io_interp/__config__.py','w')
cfgdict = {}
cfgdict['grib2io_interp_version'] = VERSION
cfgdict['has_openmp_support'] = needs_openmp
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
setup(ext_modules = ext_modules,
      long_description = long_description,
      long_description_content_type = 'text/markdown')
