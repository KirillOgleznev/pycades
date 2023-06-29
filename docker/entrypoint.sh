#!/bin/sh

while true; do
  python -m pytest tests/tests.py
  sleep 10
done