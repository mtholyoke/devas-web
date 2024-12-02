#!/bin/sh

nohup /usr/bin/python3 /opt/devas-web/superman_server.py > /opt/devas-web/logs/errors.out 2>&1 &
