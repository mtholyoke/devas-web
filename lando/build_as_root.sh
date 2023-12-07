#!/bin/sh

# Make link /opt/devas-web to /app
ln -s /app /opt/devas-web

# Install cython so that the Python packages can get installed properly
apt update
apt install --yes cython3
