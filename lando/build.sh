#!/bin/sh

pip install --upgrade pip
pip install --yes h5py==2.10.0 pyyaml==5.3 tornado==4.4.2
pip install --yes matplotlib==3.1.3 pandas = 1.0.0 pywavelets==1.1.1 


# The superman package from PyPI is missing a file; this is the easiest way to install.
cd ~
git clone git@github.com:all-umass/superman.git
cd superman
pip install -e .
