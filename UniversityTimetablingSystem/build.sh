#!/bin/bash

BUILD_TYPE="Release"

if [ "$1" == "debug" ]; then
    BUILD_TYPE="Debug"
elif [ "$1" == "release" ]; then
    BUILD_TYPE="Release"
elif [ "$1" == "build" ]; then
    BUILD_TYPE="Release"
else
    echo "Usage: $0 {build|release|debug}"
    exit 1
fi

mkdir -p build
cd build
cmake -DCMAKE_BUILD_TYPE=$BUILD_TYPE ..
make