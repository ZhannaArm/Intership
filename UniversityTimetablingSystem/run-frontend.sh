#!/bin/bash

set -e

cd frontend

echo "Installing dependencies..."
npm install vue@^3.4.37

echo "Starting development server..."
npm run serve
