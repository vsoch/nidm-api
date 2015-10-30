from setuptools.command.install import install as _install
from setuptools import setup, find_packages
import codecs
import sys
import os

# Post install script, if needed
def _post_install(dir):
    from subprocess import call
    call([sys.executable, 'post_install.py'],
         cwd=os.path.join(dir, 'nidm','script'))

class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Running post-install script...")


here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    # Application name:
    name="nidm",

    # Version number (initial):
    version="1.0.0",

    # Application author details:
    author="NIDM Working Group",
    author_email="vsochat@stanford.edu, c.m.j.maumet@warwick.ac.uk",

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
    keywords='neuroscience Prov, NIDM, Provenance',

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],

    install_requires = ['numpy','Flask','gitpython'],

    entry_points = {
        'console_scripts': [
            'nidm=nidm.scripts:main',
        ],
    },

    # This will install an updated version of nidm-queries in home
    cmdclass={'install': install},
)
