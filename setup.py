import os
import sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'ioctl', '__version__.py')) as fh:
    exec(fh.read())

tests_require = [ ]
if sys.version_info < (3, 3):
    tests_require.append('mock') # mock became available as unittest.mock from Python 3.3.

setup(
    name = 'ioctl',
    packages = find_packages(),
    version = VERSION,
    description = 'ioctl helper functions',
    license = 'MIT',
    maintainer = 'Olav Morken',
    maintainer_email = 'olavmrk@gmail.com',
    url = 'https://github.com/olavmrk/python-ioctl',
    download_url = 'https://github.com/olavmrk/python-ioctl/tarball/v{version}'.format(version=VERSION),
    tests_require = tests_require,
    test_suite = 'tests',
)
