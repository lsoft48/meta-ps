# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join, dirname
import sys
import metaps1


reqs=['requests','patool', 'sh']
#if sys.platform.startswith("linux"):
#    reqs.append('python-apt')


setup(
    name='metaps1',
    version=metaps1.__version__,
    author='LSoft',
    packages=find_packages(),
    description='1C Enterprise installer',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=reqs,
    entry_points={
        'console_scripts':
            ['meta-ps = metaps1.main:ExecuteCommand']
        }
)
