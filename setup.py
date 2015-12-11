import sys
import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup
import pkg_resources

# Shortcut for building/publishing to Pypi
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel upload')
    sys.exit()

# For making things look nice on pypi:
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError, RuntimeError):
    long_description = 'Tools for manipulating and parsing vcf files'

setup(name='vcftoolbox',
    version='1.1',
    description='Tools for manipulating and parsing vcf files',
    author = 'Mans Magnusson',
    author_email = 'mans.magnusson@scilifelab.se',
    url = 'http://github.com/moonso/vcftoolbox',
    license = 'MIT License',
    install_requires=[
        'pytest',
    ],
    packages=find_packages(
        exclude=('tests*', 'docs', 'examples', 'configs')
    ),
    keywords = ['vcf', 'parsing'],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Unix",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    long_description = long_description,
)