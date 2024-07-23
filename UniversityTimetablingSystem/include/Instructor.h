#ifndef UNIVERSITY_TIMETABLING_SYSTEM_INSTRUCTOR_H
#define UNIVERSITY_TIMETABLING_SYSTEM_INSTRUCTOR_H
#include <iostream>
#include <string>
#include <vector>
#include "/usr/local/opt/nlohmann-json/include/nlohmann/json.hpp"
#include "Course.h"
#include "TimeSlot.h"
/*
 * @class Instructor
 * @brief A class to represent an instructor with a name, availability, and preferred courses.
 *
 * @default constructor Instructor
 *
 * @constructor Instructor
 * @param name: the name of the instructor
 * @param availability: the availability of the instructor
 * @param preferredCourses: the preferred courses of the instructor
 * @brief Construct an instructor with a name, availability and preferred courses
 *
 * @method displayInfo
 * @brief Display the information of the instructor.
 *
 * @function addPreferredTimeSlot
 * @param timeSlot: The time slot to add as preferred.
 * @brief Adds a preferred time slot to the instructor's availability.
 *
 * @function addPreferredCourse
 * @param course The course to add as preferred.
 * @brief Adds a preferred course to the instructor's preferred courses.
 *
 * @getters
 * @function getName
 * @brief Retrieves the name of the instructor.
 * @return A string representing the instructor's name.
 *
 * @function getAvailability
 * @brief Retrieves the availability time slots of the instructor.
 * @return A vector of TimeSlot objects representing the instructor's availability.
 *
 * @function getPreferredCourses
 * @brief Retrieves the preferred courses of the instructor.
 * @return A vector of Course objects representing the instructor's preferred courses.
 *
 * @function toJson
 * @brief Converts the Instructor object to a JSON object.
 * @return a JSON object
 *
 * @operator==
 * @param other: The other Instructor object to compare with
 * @brief Equality operator to compare two Instructor objects.
 * @return True if the other object is equal to this object, false otherwise.
 */

class Instructor {
private:
    std::string name;
    std::vector<TimeSlot> availability;
    std::vector<Course> preferredCourses;

public:
    Instructor() = default;

    Instructor(std::string name_, std::vector<TimeSlot> availability_, std::vector<Course> preferred_courses);

    void displayInfo() const;

    void addPreferredTimeSlot(TimeSlot& timeSlot);

    void addPreferredCourse(Course& course);

    std::string getName() const;

    std::vector<TimeSlot> getAvailability() const;

    std::vector<Course> getPreferredCourses() const;

    json toJson() const;

    bool operator==(const Instructor& other) const;
};

#endif
