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
        sanitize)
            build_type="sanitize"
            ;;
        *)
            echo "Invalid argument: $1"
            echo "Usage: $0 [debug|release|sanitize]"
            exit 1
            ;;
    esac
fi

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
    sanitize)
        echo "Building in sanitize mode..."
        cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DSANITIZE=ON ..
        ;;
esac

make
