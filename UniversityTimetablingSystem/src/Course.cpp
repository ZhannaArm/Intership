#include "Course.h"

#include <iostream>
#include <utility>

Course::Course(const std::string& course_name, const std::vector<TimeSlot>& preferred_time_slots)
    : courseName(course_name), preferredTimeSlots(preferred_time_slots) {}

Course::Course(const Course& other)
    : courseName(other.courseName), preferredTimeSlots(other.preferredTimeSlots) {}

void Course::displayInfo() const {
    std::cout << "Course Name: " << courseName << std::endl;
    std::cout << "Preferred Time Slots: " << std::endl;
    for (const auto& timeSlot : preferredTimeSlots) {
        timeSlot.displayInfo();
    }
}

void Course::addPreferredTimeSlot(TimeSlot& preferredTimeSlot) {
    this->preferredTimeSlots.push_back(preferredTimeSlot);
}

std::vector<TimeSlot> Course::getPreferredTimeSlots() const { return this->preferredTimeSlots; }

std::string Course::getCourseName() const { return this->courseName; }

json Course::toJson() const {
    json timeSlotsJson = json::array();
    for (const auto& timeSlot : preferredTimeSlots) {
        timeSlotsJson.push_back(timeSlot.toJson());
    }
    return json{{COURSE_NAME, courseName}, {PREFERRED_TIME_SLOTS, timeSlotsJson}};
}

Course& Course::operator=(const Course& other) {
    if (this != &other) {
        courseName = other.courseName;
        preferredTimeSlots = other.preferredTimeSlots;
    }
    return *this;
}

bool Course::operator==(const Course& other) const { return courseName == other.courseName; }

bool Course::operator<(const Course& other) const { return this->courseName < other.courseName; }