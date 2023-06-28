#!/bin/sh

while true; do
  echo "Waiting for PostgreSql to start..."
  python tests/tests.py
  sleep 10
done