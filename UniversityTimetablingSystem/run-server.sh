#!/bin/bash

set -e

cd  backend

if [ -d "env" ]; then
    echo "Activating virtual environment..."
    source env/bin/activate
fi

echo "Making migrations..."
python3 manage.py makemigrations

echo "Applying database migrations..."
python3 manage.py migrate

echo "Starting the server..."
python3 manage.py runserver

echo "Server is running at http://127.0.0.1:8000/"