#!/bin/bash

set -e

cd frontend

echo "Installing dependencies..."
npm install vue@^3.2.13

echo "Starting development server..."
npm run serve
