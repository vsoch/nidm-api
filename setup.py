from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Application name:
    name="nidmapi",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="NIDM Working Group",
    author_email="vsochat@stanford.edu",

    # Packages
    packages=find_packages(),

    # Data files
    include_package_data=True,
    zip_safe=False,

    # Details
    url="https://github.com/incf-nidash/nidm-api",

    license="LICENSE.txt",
    description="Python module and application for running a REST API server to perform queries and visualize graphs with NIDM results, experiments, and workflows.",
    long_description=long_description,
    keywords='nidm neuroscience',

    install_requires = ['numpy','Flask','gitpython'],

    entry_points = {
        'console_scripts': [
            'nidmapi=nidmapi.scripts:main',
        ],
    },

)
