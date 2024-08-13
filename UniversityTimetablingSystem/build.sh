#!/bin/bash

build_type="release"

if [ $# -gt 0 ]; then
    case "$1" in
        debug)
            build_type="debug"
            ;;
        release)
            build_type="release"
            ;;
        *)
            echo "Invalid argument: $1"
            echo "Usage: $0 [debug|release]"
            exit 1
            ;;
    esac
fi

echo "Building GoogleTest..."
cd submodules/googletest
mkdir -p build
cd build
rm -rf CMakeCache.txt CMakeFiles
cmake -DCMAKE_INSTALL_PREFIX="../bin" ..
make
make install
cd ../../..

echo "GoogleTest installed to ${install_dir}"
mkdir -p build
cd build

case "$build_type" in
    debug)
        echo "Building in debug mode..."
        cmake -DCMAKE_BUILD_TYPE=Debug ..
        ;;
    release)
        echo "Building in release mode..."
        cmake -DCMAKE_BUILD_TYPE=Release ..
        ;;
esac

make
make install
