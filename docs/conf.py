# -*- coding: utf-8 -*-

from __future__ import division, absolute_import, print_function

AUTHOR = u'Christopher Larson'

# General configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.extlinks']

exclude_patterns = ['_build']
source_suffix = '.rst'
master_doc = 'index'

project = u'beets-kergoth'
copyright = u'2019, Christopher Larson'

version = '0.3'
release = '0.3.1'

pygments_style = 'sphinx'
