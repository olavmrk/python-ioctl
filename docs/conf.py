#!/usr/bin/env python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import ioctl.__version__

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.viewcode',
]

master_doc = 'index'

project = u'python-ioctl'

release = ioctl.__version__.VERSION
# Calculate the version based on the first two parts of the release. I.e. "1.2.3" => "1.2"
version = '.'.join(release.split('.', 3)[:2])

html_show_copyright = False
