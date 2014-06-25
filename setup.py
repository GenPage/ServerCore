#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='TechnicServerCore',
    version='0.3.0-alpha',
    author='Dylan Page',
    maintainer='Dylan Page',
    author_email='genpage@technicpack.net',
    maintainer_email='genpage@technicpack.net',	
    packages=find_packages(),

    url='http://github.com/GenPage/ServerCore/',
    license='LICENSE.txt',
    description='Custom wrapper that downloads and updates Technic modpacks specifically for servers.',
    long_description=open('README.md').read(),
    install_requires=[
        "progressbar >= 2.2",
    ],
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
