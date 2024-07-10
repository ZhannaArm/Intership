#ifndef COURSE_H
#define COURSE_H
#include <string>
#include <vector>
#include "TimeSlot.h"
#include <nlohmann/json.hpp>
/*
 * @class Course
 * @A class to represent a course with a name and preferred time slots.
 *
 * @default constructor Course
 *
 * @constructor Course
 * @param name: Name of the course
 * @param preferredTimeSlots: A vector of preferred time slots for the course.
 * @brief Construct a Course with the given name and preferred time slots.
 *
 * @method displayInfo
 * @brief Display information about the course with the given name and preferred time slots.
 *
 * @function addPreferredTimeSlot
 * @param name timeSlot: The time slot to add as preferred.
 * @brief Adds a preferred time slot to the course.
 *
 * @getters
 * @function getPreferredTimeSlots
 * @return A vector of TimeSlot objects representing the preferred time slots.
 *
 * @function getCourseName
 * @return A string describing the course
 *
 * @function toJson
 * @brief Converts the Course object to a JSON object.
 * @return a JSON object
 *
 * @operator==
 * @param other: The other Course object to compare with
 * @brief Equality operator to compare two Course objects.
 * @return True if the other object is equal to this object, false otherwise.
 *
 * @operator<
 * @param other: The other Course object to compare with
 * @brief Less-than operator to compare two Course objects for sorting.
 * @return True if this Course object is less than the other, false otherwise.
 */

class Course {
private:
    std::string courseName;
    std::vector<TimeSlot> preferredTimeSlots;

public:
    Course() = default;

    Course(std::string courseName, std::vector<TimeSlot> preferredTimeSlots);

    void displayInfo() const;

    void addPreferredTimeSlot(TimeSlot& preferredTimeSlot);

    std::vector<TimeSlot> getPreferredTimeSlots() const;

    std::string getCourseName() const;

    json toJson() const;

    bool operator==(const Course& other) const;

    bool operator<(const Course& other) const;
};

#endif
