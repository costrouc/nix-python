from setuptools import setup, find_packages, Extension
from setuptools.command import build_ext
from pybind11 import get_include

setup(
    name="nix-python",
    version="0.0.1dev",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    ext_modules=[
        Extension(
            '_nix', ['src/_nix/nix.cc'],
            include_dirs=[get_include(), '/usr/include/nix'],
            library_dirs=[],
            libraries=['nixstore'],
            language='c++',
            extra_compile_args=['-std=c++17']
        )
    ],
    cmdclass={'build_ext': build_ext.build_ext},
)
