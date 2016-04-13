# -*- coding: utf-8 -*-

from setuptools import setup,find_packages

with open("README.rst") as f:
    readme = f.read()

setup(
    name = 'IngestionPy',
    version = '0.1',
    description = "fast ingest academic documents",
    long_description = readme,
    author = "Huaiyu Yang, Jian Wu",
    author_email = "davidyangrocs@gmail.com, fanchyna@gmail.com",
    url = "https://github.com/huaiyudavid/IngestionPy",
    packages = find_packages(exclude=("test","docs")),
    test_suite="nose.collector",
    tests_require=['nose']
)

