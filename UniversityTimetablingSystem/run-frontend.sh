#!/bin/bash

set -e

cd frontend

echo "Installing dependencies..."
npm install

echo "Starting development server..."
npm run serve