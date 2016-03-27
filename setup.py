#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


from setuptools import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()

setup(
    name='cmpcsv',
    version='0.1',
    description='Simple CSV compare',
    long_description=readme,
    author='Alexey Trofimov',
    author_email='dmzkrsk@gmail.com',
    url='https://github.com/dmzkrsk/cmpcsv',
    packages=[
        'cmpcsv',
    ],
    package_dir={'cmpcsv': 'cmpcsv'},
    entry_points={
        'console_scripts': [
            'cmpcsv = cmpcsv.cmpcsv:cmpcsv_cmd',
        ],
    },
    include_package_data=True,
    install_requires=[
        'six',
    ],
    license="MIT",
    zip_safe=False,
    keywords='cmpcsv csv',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
)