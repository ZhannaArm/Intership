#include <iostream>
#include <vector>

#include "Constants.h"
#include "Course.h"
#include "Instructor.h"
#include "TimeSlot.h"
#include "University.h"

void processArgs(int argc, char** argv, University& university) {
    int i = 0;
    std::string arg = argv[i];

    if (arg == ARG_ADD_INSTRUCTOR) {
        university.loadState(RESULT_JSON);
        std::string instructorJson = argv[++i];
        json j = json::parse(instructorJson);
        std::vector<Course> preferredCourses;
        std::vector<TimeSlot> availability;

        std::string instructorName = j[NAME];
        for (const auto& courseJson : j[PREFERRED_COURSES]) {
            std::string courseName = courseJson[COURSE_NAME];
            try {
                Course course = university.getCourse(courseName);
                preferredCourses.push_back(course);
            } catch (const std::runtime_error& e) {
                std::cerr << "Error: " << e.what() << " for course " << courseName << std::endl;
            }
        }

        for (const auto& slot : j[AVAILABILITY]) {
            TimeSlot timeSlot(slot[DAY], slot[START_TIME], slot[END_TIME]);
            availability.push_back(timeSlot);
        }

        Instructor instructor(instructorName, availability, preferredCourses);
        university.addInstructor(instructor);
        university.saveState(RESULT_JSON);

    } else if (arg == ARG_ADD_COURSE) {
        university.loadState(RESULT_JSON);
        std::string courseJson = argv[++i];
        json j = json::parse(courseJson);

        std::string courseName = j[COURSE_NAME];
        std::vector<TimeSlot> preferredTimeSlots;
        for (const auto& ts : j[PREFERRED_TIME_SLOTS]) {
            TimeSlot timeSlot(ts[DAY], ts[START_TIME], ts[END_TIME]);
            preferredTimeSlots.push_back(timeSlot);
        }

        Course course(courseName, preferredTimeSlots);
        std::cout << "COURSE: ";
        course.displayInfo();
        university.addCourse(course);
        university.saveState(RESULT_JSON);

    } else if (arg == ARG_ADD_TIME_SLOT) {
        university.loadState(RESULT_JSON);
        std::string timeSlotArg = argv[++i];
        json timeSlotJson = json::parse(timeSlotArg);

        for (const auto& slot : timeSlotJson) {
            TimeSlot timeSlot(slot[DAY], slot[START_TIME], slot[END_TIME]);
            university.addTimeSlot(timeSlot);
        }
        university.saveState(RESULT_JSON);

    } else if (arg == ARG_SCHEDULE) {
        university.loadState(RESULT_JSON);
        auto schedule = university.schedule();
        university.saveState(RESULT_JSON);

        json universityData = university.scheduleToJsonFormat();

        std::cout << universityData.dump(4) << std::endl;

    } else if (arg == ARG_CLEAR_FILE) {
        std::ofstream file(RESULT_JSON, std::ofstream::trunc);
        if (file) {
            json emptyJson = json::object();
            file << emptyJson.dump(4);
            file.close();
            std::cout << "File cleared and initialized with an empty JSON object." << std::endl;
        } else {
            std::cerr << "Failed to open file " << RESULT_JSON << " for clearing." << std::endl;
        }

    } else if (arg == ARG_SHOW) {
        university.loadState(RESULT_JSON);

        json universityData;

        universityData[COURSES] = nlohmann::json::array();
        for (const auto& course : university.getCourses()) {
            nlohmann::json courseData;
            courseData[COURSE_NAME] = course.getCourseName();
            universityData[COURSES].push_back(courseData);
        }

        universityData[INSTRUCTORS] = nlohmann::json::array();
        for (const auto& instructor : university.getInstructors()) {
            nlohmann::json instructorData;
            instructorData[NAME] = instructor.getName();
            universityData[INSTRUCTORS].push_back(instructorData);
        }

        universityData[TIME_SLOTS] = nlohmann::json::array();
        for (const auto& slot : university.getTimeSlots()) {
            nlohmann::json slotData;
            slotData[DAY] = slot.getDay();
            slotData[START_TIME] = slot.getStartTime();
            slotData[END_TIME] = slot.getEndTime();
            universityData[TIME_SLOTS].push_back(slotData);
        }

        std::cout << universityData.dump(4) << std::endl;
        university.saveState(RESULT_JSON);

    } else {
            std::cerr << "Unknown argument: " << arg << std::endl;
    }
}

int main(int argc, char** argv) {
    University university;

    processArgs(argc, argv, university);
    return 0;
}