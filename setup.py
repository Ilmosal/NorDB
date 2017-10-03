from distutils.core import setup

setup(
	name="NorDB",
	version="0.1.1",
	author="Ilmo Salmenperä",
	author_email="ilmo.salmenpera@helsinki.fi",
	packages=["nordb", "nordb/database", "nordb/io", "nordb/validation", "nordb/sql"],
	scripts=["bin/run.py"],
	url="http://github.com/MrCubanfrog/NorDB",
	licence="LICENSE",
	description="Library for handling a seismic event database based on the nordic format",
	install_requires=[
		"psycopg2",
	],
	long_description=open("README.md").read(),
	entry_points='''
		[console_scripts]
		nordb=bin.run.py:nordb
	''',
)
