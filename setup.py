from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

extensions = [
    Extension("ckmeans_v3", ["ckmeans_v3.pyx"],
        include_dirs = ["/usr/local/lib/python2.7/site-packages/numpy/core/include"],
        #libraries = ["numpy"],
        library_dirs = ["/usr/local/lib/python2.7/site-packages/numpy/core/lib"]),
]

setup(
    name = "ckmeans_v3",
    ext_modules = cythonize(extensions),
)