from setuptools import setup, find_packages

VERSION = '0.0'

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
    tests_require = [ 'mock' ],
    test_suite = 'tests',
)
