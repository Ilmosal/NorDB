from distutils.core import setup

setup(
	name="NorDB",
	version="0.1.0",
	author="Ilmo Salmenperä",
	author_email="ilmo.salmenpera@helsinki.fi",
	packages=["nordb", "nordb/database", "nordb/io", "nordb/validation", "nordb/nordsql"],
	scripts=["bin/run.py"],
	url="http://github.com/MrCubanfrog/NorDB.git",
	licence="LICENSE",
	description="Library for handling a seismic event database based on the nordic format",
	long_description=open("README.md").read(),
)
