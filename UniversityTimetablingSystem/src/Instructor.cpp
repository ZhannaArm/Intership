#include "Instructor.h"

#include <utility>

Instructor::Instructor(std::string name_, std::vector<TimeSlot> availability_,
                       std::vector<Course> preferred_courses)
    : name(std::move(name_)),
      availability(std::move(availability_)),
      preferredCourses(std::move(preferred_courses)) {}

void Instructor::displayInfo() const {
    std::cout << "Instructor Name: " << name << std::endl;
    std::cout << "Availability:" << std::endl;
    for (const auto& timeSlot : availability) {
        timeSlot.displayInfo();
    }
    std::cout << "Preferred Courses:" << std::endl;
    for (const auto& course : preferredCourses) {
        course.displayInfo();
    }
}

std::string Instructor::getName() const { return this->name; }

std::vector<TimeSlot> Instructor::getAvailability() const { return this->availability; }

std::vector<Course> Instructor::getPreferredCourses() const { return this->preferredCourses; }

void Instructor::addPreferredTimeSlot(TimeSlot& timeSlot) {
    this->availability.push_back(timeSlot);
}

void Instructor::addPreferredCourse(Course& course) { this->preferredCourses.push_back(course); }

json Instructor::toJson() const {
    json availabilityJson = json::array();
    for (const auto& timeSlot : availability) {
        availabilityJson.push_back(timeSlot.toJson());
    }

    json coursesJson = json::array();
    for (const auto& course : preferredCourses) {
        coursesJson.push_back(course.toJson());
    }

    return json{
        {NAME, name}, {AVAILABILITY, availabilityJson}, {PREFERRED_COURSES, coursesJson}};
}

bool Instructor::operator==(const Instructor& other) const { return this->name == other.name; }