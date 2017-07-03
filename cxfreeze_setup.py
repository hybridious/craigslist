#!/usr/bin/env python3

from setuptools import find_packages
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["lxml._elementpath", "asyncio", "idna"]}

readme = open('README.rst').read()
version = exec(open('craigslist/version.py').read())

setup(
    name='craigslist',
    version=__version__,
    description='Python wrapper for craigslist.',
    long_description=readme,
    author='Al Johri',
    author_email='al.johri@gmail.com',
    url='https://github.com/AlJohri/craigslist',
    license='MIT',
    packages=find_packages(),
    package_data={'craigslist': ['data/*.json']},
    install_requires=['requests', 'cssselect', 'lxml', 'blessings', 'arrow'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'craigslist=craigslist.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
    ],
    options = {"build_exe": build_exe_options},
    executables = [Executable("craigslist/cli.py", base=None)]
)
