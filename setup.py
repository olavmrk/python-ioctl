import os
import sys
from setuptools import setup, find_packages

tests_require = [ ]
if sys.version_info < (3, 3):
    tests_require.append('mock') # mock became available as unittest.mock from Python 3.3.

setup(
    name = 'ioctl',
    packages = find_packages(),
    use_scm_version = True,
    description = 'ioctl helper functions',
    license = 'MIT',
    maintainer = 'Olav Morken',
    maintainer_email = 'olavmrk@gmail.com',
    url = 'https://github.com/olavmrk/python-ioctl',
    download_url = 'https://github.com/olavmrk/python-ioctl/releases',
    setup_requires = [ 'setuptools_scm' ],
    tests_require = tests_require,
    test_suite = 'tests',
)
