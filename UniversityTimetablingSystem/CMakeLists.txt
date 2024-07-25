cmake_minimum_required(VERSION 3.17)
project(UniversityTimetablingSystem)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

#Add subdirectory for argparse library
add_subdirectory(argparse)

#Include directories for header files
include_directories(${CMAKE_SOURCE_DIR}/argparse)
include_directories(${CMAKE_SOURCE_DIR}/nlohmann)

#Include nlohmann-json library
#set(NLOHMANN_JSON_INCLUDE_DIR "/usr/local/opt/nlohmann-json/include")
#include_directories(${NLOHMANN_JSON_INCLUDE_DIR})

#Add source files for the UniversityTimetablingLib library
add_library(UniversityTimetablingLib SHARED
        src/Course.cpp
        src/TimeSlot.cpp
        src/Instructor.cpp
        src/University.cpp
        )

#Include directories for the UniversityTimetablingLib library
target_include_directories(UniversityTimetablingLib PUBLIC
        ${CMAKE_SOURCE_DIR}/src
        ${CMAKE_SOURCE_DIR}/include
        ${CMAKE_SOURCE_DIR}/nlohmann
        ${CMAKE_SOURCE_DIR}/argparse
        )

#Add executable for the main application
add_executable(UniversityTimetablingSystem src/main.cpp) #Creates an executable from main.cpp
target_link_libraries(UniversityTimetablingSystem PRIVATE UniversityTimetablingLib) #Links an executable file to a dynamic library

#Add Google test
#add_subdirectory(googletest)
#include_directories(googletest/googletest/include)

#Add executable for running tests
#add_executable(runTests tests/test_University.cpp)
#target_link_libraries(runTests PRIVATE UniversityTimetablingLib gtest gtest_main)

#Enable testing
#enable_testing()

#Add test
#add_test(NAME runTests COMMAND runTests)
