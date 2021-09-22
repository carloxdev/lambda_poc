#!/bin/sh

echo "Waiting for DB to start..."
chmod +x wait-for
./wait-for db:3306

echo "Runing code..."
coverage run --source=. -m unittest --v test/test_child_app.py
