cmake_minimum_required(VERSION 3.17)
project(UniversityTimetablingSystem)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-attributes")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fno-inline")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2 -Wno-inline -DNDEBUG")
set(CMAKE_CXX_FLAGS_SANITIZE "${CMAKE_CXX_FLAGS_DEBUG} -fsanitize=address,undefined")

#Add subdirectory for argparse and nlohmann libraries
add_subdirectory(submodules/argparse)
add_subdirectory(submodules/nlohmann)

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
        ${CMAKE_SOURCE_DIR}/submodules/nlohmann/include
        ${CMAKE_SOURCE_DIR}/submodules/argparse
        )

#Add executable for the main application
add_executable(UniversityTimetablingSystem src/main.cpp) #Creates an executable from main.cpp
target_link_libraries(UniversityTimetablingSystem PRIVATE UniversityTimetablingLib) #Links an executable file to a dynamic library

#Add Google test
add_subdirectory(submodules/googletest)
include_directories(submodules/googletest/googletest/include)

#Add executable for running tests
add_executable(runTests tests/test_University.cpp)
target_link_libraries(runTests PRIVATE UniversityTimetablingLib gtest gtest_main)

#Install UniversityTimetablingLib to lib directory
install(TARGETS UniversityTimetablingLib
        LIBRARY DESTINATION ${CMAKE_SOURCE_DIR}/lib)

#Install UniversityTimetablingSystem executable to bin directory
install(TARGETS UniversityTimetablingSystem
        RUNTIME DESTINATION ${CMAKE_SOURCE_DIR}/bin)

#Install runTests executable to bin directory
install(TARGETS runTests
        RUNTIME DESTINATION ${CMAKE_SOURCE_DIR}/bin)

#Enable testing
#enable_testing()

#Add test
#add_test(NAME runTests COMMAND runTests)
