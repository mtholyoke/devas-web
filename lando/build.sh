#!/bin/sh

# Install python packages
pip install --upgrade pip
pip install h5py==3.6.0 pyyaml==5.3 tornado==4.4.2
pip install matplotlib==3.1.3 pandas==1.1.5 pywavelets==1.1.1 


# The superman package from PyPI is missing a file; this is the easiest way to install.
cd ~
git clone git@github.com:all-umass/superman.git
cd superman
git apply /app/lando/all_umass-superman-cimport.patch
pip install -e .
