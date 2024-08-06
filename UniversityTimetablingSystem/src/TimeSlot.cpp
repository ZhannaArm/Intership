#include "TimeSlot.h"

#include <utility>

TimeSlot::TimeSlot(std::string day_, std::string start_time, std::string end_time)
    : day(std::move(day_)), startTime(std::move(start_time)), endTime(std::move(end_time)) {}

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