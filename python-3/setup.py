#!/usr/bin/env python

from distutils.core import setup

setup(
    name='fastspring',
    version="0.0.1",
    description='A module for working with the FastSpring orders and subscriptopns API',
    author='Artlogic Media Limited',
    author_email='support@artlogic.net',
    url='https://github.com/artlogicmedia/fastspring',
    packages = ['fastspring'],
    install_requires = ['xmltodict'],
    license = "MIT or GPLv2",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'License :: OSI Approved :: MIT License',
    ],
)
