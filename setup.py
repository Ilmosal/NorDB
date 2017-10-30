from setuptools import setup, find_packages

setup(
    name="NorDB",
    version="0.1.2",
    author="Ilmo Salmenperä",
    author_email="ilmo.salmenpera@helsinki.fi",
    packages=find_packages(),
    include_package_data=True,
    url="http://github.com/MrCubanfrog/NorDB",
    licence="LICENSE",
    description="Library for handling a seismic event database based on the nordic format",
    install_requires=[
        "psycopg2",
        "Click",
        "lxml",
    ],
    long_description=open("README.md").read(),
    entry_points='''
        [console_scripts] 
        nordb=nordb.bin.NorDB:cli
    ''',
)
