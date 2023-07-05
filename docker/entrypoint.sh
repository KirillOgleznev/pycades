#!/bin/sh

#python setup.py bdist_wheel
#pip install ./wheelhouse/*.whl

while true; do
  python -m pytest tests/tests.py
  sleep 10
done
