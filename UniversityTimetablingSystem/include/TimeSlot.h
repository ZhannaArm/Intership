#ifndef UNIVERSITY_TIMETABLING_SYSTEM_TIMESLOT_H
#define UNIVERSITY_TIMETABLING_SYSTEM_TIMESLOT_H
#include <iostream>
#include "/usr/local/opt/nlohmann-json/include/nlohmann/json.hpp"
#include <string>
/*
 * @class TimeSlot
 * @brief A class to represent a time slot with a day, start time, and end time.
 *
 * @default constructor TimeSlot
 *
 * @constructor TimeSlot
 * @param day: Day of time slot
 * @param start: Where to start the time slot
 * @param end: Where to end the time slot
 * @brief Construct a time slot with a day, start time, and end time
 *
 * @method displayInfo
 * @brief Display the time slot information for a day, start time, and end time
 *
 * @getters
 * @function getDay
 * @return A day of the time slot
 *
 * @function getStartTime
 * @return A start time of the time slot
 *
 * @function getEndTime
 * @return A end time of the time slot
 *
 * @function toJson
 * @brief Converts the TimeSlot object to a JSON object.
 * @return a JSON object
 *
 * @operator==
 * @param other: other TimeSlot object for compare with
 * @brief Equality operator to compare two TimeSlot objects.
 * @return True if the two TimeSlot objects are equal, false otherwise.
 */

using json = nlohmann::json;

class TimeSlot {
private:
    std::string day;
    std::string startTime;
    std::string endTime;
public:
    TimeSlot() = default;

    TimeSlot(std::string day_, std::string start_time, std::string end_time);

    void displayInfo() const;

    std::string getDay() const;

    std::string getStartTime() const;

    std::string getEndTime() const;

    json toJson() const;

    bool operator==(const TimeSlot& other) const;
};
#endif
