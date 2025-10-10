import glob
import os
import sys

from Cython.Build import cythonize
from setuptools import Extension, setup

if sys.platform.startswith("win"):
    openmp_arg = '/openmp'
else:
    openmp_arg = '-fopenmp'

# Collect python source files in this directory to cythonize, excluding setup.py
sources = [f for f in glob.glob('*.py') if os.path.basename(f) != 'setup.py']

extensions = cythonize(
    Extension('*', sources, extra_compile_args=[openmp_arg], extra_link_args=[openmp_arg]),
    annotate=True,
)

setup(
    name='pyraytracing_cy',
    ext_modules=extensions,
    zip_safe=False,
)
