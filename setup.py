# -*- coding: utf-8 -*-

import os
import sys
import re

from setuptools import setup, find_packages


def get_version():
    """
    Returns version string by using regex to parse package init file for __version__ variable
    """
    import re
    
    vfile   =   os.path.join( 'src', 'bdcapi', '__init__.py' )
    regex   =   r'^(?:__version__)(?:\s*)=(?:\s*)(?:[\'"]([^\'"]*)[\'"]).*$'
    
    with open(vfile, 'rt') as fp:
        for line in fp.readlines():
            mo = re.search(regex, line, re.M)
            if mo:
                return mo.group(1)
    raise RuntimeError('Unable to find version string in %s.' % (vfile,))


requirements = [
    'Click',
    'click-plugins',
    'pandas',
    'requests',
    'PyYAML',
    'importlib-resources; python_version == "3.8"' ]

setup(
    name='bdcapi',
    version=get_version(),
    requires_python='>=3.8',
    description='BDCAPI is a tool to interface with the publicly-accessible APIs for the Broadband Data Collection (BDC) system',
    author='Jonathan McCormack',
    url='http://github.com/jonathanmccormack/bdcapi',
    packages=find_packages(where='src'),
    package_dir={ '': 'src' },
    package_data={ 'bdcapi': [ 'pkg_data/*.yml' ] },
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        bdcapi=bdcapi:cli
        ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommnications Industry',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Communications',
        'Topic :: Utilities' ])


#
