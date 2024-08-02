#ifndef UNIVERSITY_TIMETABLING_SYSTEM_UNIVERSITY_H
#define UNIVERSITY_TIMETABLING_SYSTEM_UNIVERSITY_H
#include <iostream>
#include "nlohmann/json.hpp"
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
 * I have two solutions for schedule planning(main algorithm - schedule, brute force algorithm - schedule_bruteForce)
 * @method schedule
 * @brief Creates a schedule mapping courses to instructors and time slots.
 * @return A University schedule.
 *
 * @method schedule_bruteForce
 * @brief Creates a schedule mapping courses using an algorithm brute force to instructors and time slots.
 *
 * @function displaySchedule
 * @brief Displays the current course schedule from std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>> Schedule.
 *
 * @function displayScheduleMap
 * @brief Displays the current course schedule from std::map<Course, std::pair<Instructor, TimeSlot>> scheduleMap.
 */
class University {
private:
    std::vector<Course> courses;
    std::vector<Instructor> instructors;
    std::vector<TimeSlot> timeSlots;
    std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>> Schedule;
    //for brute force algorithm
    std::map<Course, std::pair<Instructor, TimeSlot>> scheduleMap;

    static double calculateScheduleCost(const std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>>& schedule);
public:
    void addCourse(const Course& course);

    void addInstructor(const Instructor& instructor);

    void addTimeSlot(const TimeSlot& timeSlot);

    std::vector<TimeSlot> getTimeSlots() const;

    std::vector<Instructor> getInstructors() const;

    std::vector<Course> getCourses() const;

    bool courseExists(const std::string& courseName) const;

    const Course* getCourse(const std::string& courseName) const;

    void saveState(const std::string& filename);

    void loadState(const std::string& filename);

    void displayInfo() const;

    std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>> schedule();

    std::vector<std::tuple<std::string, std::string, std::string>> scheduleToJsonFormat() const;

    void schedule_bruteForce(); //the second solution

    void displaySchedule() const;

    void displayScheduleMap() const;
};

#endif