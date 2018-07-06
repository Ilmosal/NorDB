# -*- coding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name="NorDB",
    version="0.3.3",
    python_requires='>3.6.0',
    author="Ilmo Salmenperä",
    author_email="ilmo.salmenpera@helsinki.fi",
    packages=find_packages(),
    include_package_data=True,
    url="http://github.com/MrCubanfrog/NorDB",
    license="LICENSE",
    description="Library for handling a seismic event database based on the nordic format",
    setup_requires=[
        "pytest-runner",
    ],
    install_requires=[
        "psycopg2-binary",
        "Click",
        "lxml",
        "Sphinx",
        "unidecode",
        "alabaster",
        "numpy"
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
    ],
    long_description=open("README.md").read(),
    entry_points='''
        [console_scripts] 
        nordb=nordb.bin.NorDB:cli
    ''',
)
