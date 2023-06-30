#!/bin/sh

while true; do
  /opt/python/cp37-cp37m/bin/python -m pytest tests/tests.py
  sleep 10
done