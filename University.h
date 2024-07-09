#ifndef INTERSHIP_UNIVERSITY_H
#define INTERSHIP_UNIVERSITY_H
#include <iostream>
#include "/usr/local/opt/nlohmann-json/include/nlohmann/json.hpp"
#include <string>
#include <vector>
#include <fstream>
#include <map>
#include <algorithm>
#include <random>
#include <cmath>
#include <limits>
#include <ctime>
#include <cstdlib>
#include "Instructor.h"
#include "TimeSlot.h"
#include "Course.h"
/*
 * @class University
 * @brief A class to manage courses, instructors, time slots, and course scheduling.
 *
 * @method addCourse
 * @param course: The course to add.
 * @brief Adds a course to the university.
 *
 * @method addInstructor
 * @param instructor: The instructor to add.
 * @brief Adds a course to the university.
 *
 * @method addTimeSlot
 * @param timeSlot: The time slot to add.
 * @brief Adds a time slot to the university.
 *
 * @function getTimeSlots
 * @brief Retrieves the list of time slots in the university.
 * @return A vector of TimeSlot objects.
 *
 * @function getInstructors
 * @brief Retrieves the list of instructors in the university.
 * @return A vector of Instructor objects.
 *
 * @function getCourses
 * @brief Retrieves the list of courses in the university.
 * @return A vector of Course objects.
 *
 * @method saveState
 * @param filename The name of the file to save the state to.
 * @brief Saves the current state of the university to a file with a JSON format.
 *
 * @method loadState
 * @param filename The name of the file to load the state from.
 * @brief Loads the state of the university from a file with a JSON format.
 *
 * @function displayInfo
 * @brief Displays the information of the university.
 *
 * @method schedule
 * @brief Creates a schedule mapping courses to instructors and time slots.
 * @return A University schedule
 *
 * @function displaySchedule
 * @brief Displays the current course schedule.
 */
class University {
private:
    std::vector<Course> courses;
    std::vector<Instructor> instructors;
    std::vector<TimeSlot> timeSlots;
    std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>> Schedule;

    //for bad algorithm
    //std::map<Course, std::pair<Instructor, TimeSlot>> scheduleMap;

    static double calculateScheduleCost(const std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>>& schedule);
public:
    void addCourse(const Course& course);

    void addInstructor(const Instructor& instructor);

    void addTimeSlot(const TimeSlot& timeSlot);

    std::vector<TimeSlot> getTimeSlots() const;

    std::vector<Instructor> getInstructors() const;

    std::vector<Course> getCourses() const;

    void saveState(const std::string& filename);

    void loadState(const std::string& filename);

    void displayInfo() const;

    std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>> schedule();

    void displaySchedule() const;
};

#endif