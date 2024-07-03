project('grib2io_interp',
        ['c', 'fortran'],
        version : run_command(
          ['python', '-c', 'print(open("VERSION").readline(), end="")'],
          check: true
        ).stdout().strip(),
        meson_version: '>= 1.1.0',
        default_options : [
                            'warning_level=3',
                            'buildtype=release',
                          ])

fs = import('fs')

fc = meson.get_compiler('fortran')
cc = meson.get_compiler('c')

py = import('python').find_installation(pure: false)
py_dep = py.dependency()

incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
  check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy)
np_dep = declare_dependency(include_directories: inc_np)

incdir_f2py = incdir_numpy / '..' / '..' / 'f2py' / 'src'
inc_f2py = include_directories(incdir_f2py)
fortranobject_c = incdir_f2py / 'fortranobject.c'

inc_np = include_directories(incdir_numpy, incdir_f2py)
# gh-25000
quadmath_dep = fc.find_library('quadmath', required: false)

omp_dep = dependency('openmp', language: 'fortran', required: false)

# Find the ip_4 library.  The current code only finds the correct path if you
# are using a conda environment.  This is OK since it is only used for
# building.
prefix = run_command(py,
  ['-c', 'import sys; print(sys.prefix)'],
  check : false
).stdout().strip()

search_dirs = [
  prefix,
  '/usr' / 'local',
  '/sw',
  '/opt',
  '/opt' / 'local',
  '/opt' / 'homebrew',
  '/usr',
]

# Need to constrain this array to only directories that exist.
# That is what cc.find_library(..., header_include_directories: ip4_inc_dirs, ...) expects.
ip4_inc_dirs = []
ip4_inc_dirs_str = []
foreach d : search_dirs
  if fs.is_dir(d / 'include_4')
    ip4_inc_dirs += include_directories(d / 'include_4')
    ip4_inc_dirs_str += d / 'include_4'
  endif
endforeach

# Do that same thing for the lib directories, however, this works fine
# unfiltered in cc.find_library(..., dirs: lib_dirs, ...)
lib_dirs = []
foreach d : search_dirs
  if fs.is_dir(d / 'lib')
    lib_dirs += d / 'lib'
  endif
endforeach

ip4_link_lib = cc.find_library('ip_4',
  static: false,
  required: true,
  dirs: lib_dirs,
  has_headers: ['iplib.h'],
  header_include_directories: ip4_inc_dirs,
  )

ftn_sources = [
  'src' / 'interpolate' / 'interpolate.f90'
]

grib2io_interp_source = custom_target('interpolatemodule',
  input : ftn_sources,
  output : [
    'interpolatemodule.c',
    'interpolate-f2pywrappers.f',
  ],
  command : [py,
    '-m', 'numpy.f2py',
    '@INPUT@',
    '-m', 'interpolate',
    '--lower',
  ])

inc_np = include_directories(incdir_numpy, incdir_f2py, ip4_inc_dirs_str)

py.extension_module('interpolate',
  ftn_sources,
  fortranobject_c,
  grib2io_interp_source,
  include_directories: inc_np,
  dependencies : [py_dep, ip4_link_lib, quadmath_dep, omp_dep],
  install : true,
  subdir: 'grib2io_interp'
)

py.install_sources('src' / 'grib2io_interp' / '__init__.py',
  subdir: 'grib2io_interp')
