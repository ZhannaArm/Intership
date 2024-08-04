#include "Course.h"

#include <iostream>
#include <utility>

Course::Course(std::string course_name, std::vector<TimeSlot> preferred_time_slots)
    : courseName(std::move(course_name)), preferredTimeSlots(std::move(preferred_time_slots)) {}

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

bool Course::operator==(const Course& other) const { return courseName == other.courseName; }

bool Course::operator<(const Course& other) const { return this->courseName < other.courseName; }