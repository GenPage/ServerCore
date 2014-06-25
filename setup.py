#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name='TechnicServerCore',
    version='0.3.1-alpha',
    author='Dylan Page',
    maintainer='Dylan Page',
    author_email='genpage@technicpack.net',
    maintainer_email='genpage@technicpack.net',	
    packages=find_packages(),

    url='http://github.com/GenPage/ServerCore/',
    license='MIT',
    description='Custom wrapper that downloads and updates Technic modpacks specifically for servers.',
    long_description=read('README.rst'),
    install_requires=[
        "progressbar >= 2.2",
    ],
    entry_points={
        'console_scripts': ['TechnicServerCore = servercore.ServerCore:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Terminals'
    ],
)
