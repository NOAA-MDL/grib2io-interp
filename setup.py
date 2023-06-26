from numpy.distutils.core import Extension, setup
from os import environ
import configparser
import glob
import numpy
import os
import platform
import sys
import sysconfig

VERSION = '1.0.0rc1'

# ----------------------------------------------------------------------------------------
# Class to parse the setup.cfg
# ----------------------------------------------------------------------------------------
class _ConfigParser(configparser.ConfigParser):
    def getq(self, s, k, fallback):
        try:
            return self.get(s, k)
        except:
            return fallback

# ----------------------------------------------------------------------------------------
# Setup find_library functions according system.
# ----------------------------------------------------------------------------------------
system = platform.system()
if system == 'Linux':
    def _find_library_linux(name):
        import subprocess
        result = subprocess.run(['/sbin/ldconfig','-p'],stdout=subprocess.PIPE)
        libs = [i.replace(' => ','#').split('#')[1] for i in result.stdout.decode('utf-8').splitlines()[1:-1]]
        try:
            return [l for l in libs if name in l][0]
        except IndexError:
            return None
    find_library = _find_library_linux
elif system == 'Darwin':
    from ctypes.util import find_library

# ---------------------------------------------------------------------------------------- 
# Read setup.cfg. Contents of setup.cfg will override env vars.
# ----------------------------------------------------------------------------------------
setup_cfg = environ.get('GRIB2IO_SETUP_CONFIG', 'setup.cfg')
config = _ConfigParser()
if os.path.exists(setup_cfg):
    sys.stdout.write('Reading from setup.cfg...')
    config.read(setup_cfg)

# ---------------------------------------------------------------------------------------- 
# Get NCEPLIBS-sp library info. This library is a required for interpolation.
# ---------------------------------------------------------------------------------------- 
libdirs = []
incdirs = []
libraries = ['sp_4','ip_4']
sp_dir = config.getq('directories', 'sp_dir', environ.get('SP_DIR'))
if os.path.exists(os.path.join(sp_dir,'lib')):
    sp_libdir = os.path.join(sp_dir,'lib')
elif os.path.exists(os.path.join(sp_dir,'lib64')):
    sp_libdir = os.path.join(sp_dir,'lib64')
libdirs.append(sp_libdir)

# ---------------------------------------------------------------------------------------- 
# Get NCEPLIBS-ip library info. This library is a required for interpolation.
# ---------------------------------------------------------------------------------------- 
ip_dir = config.getq('directories', 'ip_dir', environ.get('IP_DIR'))
ip_libdir = config.getq('directories', 'ip_libdir', environ.get('IP_LIBDIR'))
ip_incdir = config.getq('directories', 'ip_incdir', environ.get('IP_INCDIR'))
if ip_libdir is None and ip_dir is not None:
    libdirs.append(os.path.join(ip_dir,'lib'))
    libdirs.append(os.path.join(ip_dir,'lib64'))
else:
    libdirs.append(ip_libdir)
if ip_incdir is None and ip_dir is not None:
    incdirs.append(os.path.join(ip_dir,'include_4'))
else:
    incdirs.append(ip_incdir)

# ---------------------------------------------------------------------------------------- 
# Define interpolation NumPy extension module.
# ---------------------------------------------------------------------------------------- 
interpext = Extension(name = 'grib2io_interp.interpolate',
                      sources = ['src/interpolate.pyf','src/interpolate.f90'],
                      extra_f77_compile_args = ['-O3','-fopenmp'],
                      extra_f90_compile_args = ['-O3','-fopenmp'],
                      include_dirs = incdirs,
                      library_dirs = libdirs,
                      runtime_library_dirs = libdirs,
                      libraries = libraries)

# ----------------------------------------------------------------------------------------
# Define testing class
# ----------------------------------------------------------------------------------------
#class TestCommand(Command):
#    user_options = []
#    def initialize_options(self):
#        pass
#    def finalize_options(self):
#        pass
#    def run(self):
#        import sys, subprocess
#        for f in glob.glob('./tests/*.py'):
#            raise SystemExit(subprocess.call([sys.executable,f]))
#cmdclass['test'] = TestCommand

# ----------------------------------------------------------------------------------------
# Run setup
# ----------------------------------------------------------------------------------------
setup(name              = 'grib2io_interp',
      version           = VERSION,
      description       = 'Interpolation component for grib2io',
      author            = 'Eric Engle',
      author_email      = 'eric.engle@noaa.gov',
      url               = 'https://github.com/NOAA-MDL/grib2io-interp',
      download_url      = 'http://python.org/pypi/grib2io-interp',
      classifiers       = ['Development Status :: 4 - Beta',
                           'Environment :: Console',
                           'Programming Language :: Python :: 3',
                           'Programming Language :: Python :: 3 :: Only',
                           'Programming Language :: Python :: 3.8',
                           'Programming Language :: Python :: 3.9',
                           'Programming Language :: Python :: 3.10',
                           'Programming Language :: Python :: 3.11',
                           'Intended Audience :: Science/Research',
                           'License :: OSI Approved',
                           'Topic :: Software Development :: Libraries :: Python Modules'],
      ext_modules       = [interpext])
