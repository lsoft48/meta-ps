# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join, dirname
import sys
import metasites1


reqs=['requests']

e_reqs={
    'testing': ['pytest']
}


setup(
    name='metasites1',
    version=metasites1.__version__,
    author='LSoft',
    packages=find_packages(),
    description='1C site connetor',
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    install_requires=reqs,
    extras_require=e_reqs,
    entry_points={}
)
