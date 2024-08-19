#include "TimeSlot.h"

TimeSlot::TimeSlot(const std::string& day_, const std::string& start_time,
                   const std::string& end_time)
    : day(day_), startTime(start_time), endTime(end_time) {}

TimeSlot::TimeSlot(const TimeSlot& other)
    : day(other.day), startTime(other.startTime), endTime(other.endTime) {}

TimeSlot& TimeSlot::operator=(const TimeSlot& other) {
    if (this != &other) {
        day = other.day;
        startTime = other.startTime;
        endTime = other.endTime;
    }
    return *this;
}

void TimeSlot::displayInfo() const {
    std::cout << "Day: " << day << ", Start Time: " << startTime << ", End Time: " << endTime
              << std::endl;
}

std::string TimeSlot::getDay() const { return this->day; }

std::string TimeSlot::getStartTime() const { return this->startTime; }

std::string TimeSlot::getEndTime() const { return this->endTime; }

json TimeSlot::toJson() const {
    return json{{DAY, day}, {START_TIME, startTime}, {END_TIME, endTime}};
}

bool TimeSlot::operator==(const TimeSlot& other) const {
    return this->day == other.day && this->startTime == other.startTime &&
           this->endTime == other.endTime;
}