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
link_lib = cc.find_library('ip_4', static: false, required: true, dirs: prefix / 'lib')
incdir_ip = prefix / 'include_4'

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

inc_np = include_directories(incdir_numpy, incdir_f2py, incdir_ip)

py.extension_module('interpolate',
  ftn_sources,
  fortranobject_c,
  grib2io_interp_source,
  include_directories: inc_np,
  dependencies : [py_dep, link_lib, quadmath_dep, omp_dep],
  install : true,
  subdir: 'grib2io_interp'
)

py.install_sources('src' / 'grib2io_interp' / '__init__.py',
  subdir: 'grib2io_interp')
