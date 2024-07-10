cmake_minimum_required(VERSION 3.17)
project(intership)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_library(nlohmann_json INTERFACE)
target_include_directories(nlohmann_json INTERFACE "/usr/local/opt/nlohmann-json/include")

add_executable(intership src/main.cpp src/Course.cpp src/TimeSlot.cpp src/Instructor.cpp src/University.cpp src/University.h src/Course.h src/TimeSlot.h src/Instructor.h src/University.h)
target_link_libraries(intership PRIVATE nlohmann_json)

# Add Google Test
add_subdirectory(googletest)
include_directories(googletest/googletest/include)

# Add test executable
add_executable(runTests tests/test_University.cpp src/Course.cpp src/TimeSlot.cpp src/Instructor.cpp src/University.cpp src/University.h src/Course.h src/TimeSlot.h src/Instructor.h src/University.h)
target_link_libraries(runTests gtest gtest_main nlohmann_json)

# Enable testing
enable_testing()

# Add test
add_test(NAME runTests COMMAND runTests)
