#include <iostream>
#include <vector>

#include "Constants.h"
#include "Course.h"
#include "Instructor.h"
#include "TimeSlot.h"
#include "University.h"
#include "argparse.h"

int main(int argc, char** argv) {
    argparse::ArgumentParser program("UniversityTimetablingSystem", "University");

    program.add_argument(ARG_ADD_INSTRUCTOR, "Add a new instructor", false);
    program.add_argument(ARG_ADD_COURSE, "Add a new course", false);
    program.add_argument(ARG_ADD_TIME_SLOT, "Add a new time slot", false);
    program.add_argument(ARG_SCHEDULE, "Generate the schedule", false);
    program.add_argument(ARG_CLEAR_FILE, "Clear the result.json file", false);
    program.add_argument(ARG_SHOW, "Show the university information", false);
    program.add_argument(ARG_AVAILABILITY, "Add instructor's availability", false);
    program.add_argument(ARG_PREFERRED_COURSES, "Add instructor's preferred courses", false);
    program.add_argument(ARG_PREFERRED_TIME_SLOTS, "Add course's preferred time slots", false);

    auto result = program.parse(argc, const_cast<const char**>(argv));
    if (result) {
        std::cerr << "Error: " << result.what() << std::endl;
        program.print_help();
        return 1;
    }
    University rau;
    rau.loadState(RESULT_JSON);

    if (program.exists(ARG_ADD_INSTRUCTOR)) {
        auto instructorName = program.get<std::string>(ADD_INSTRUCTOR);
        std::vector<Course> preferredCourses;
        std::vector<TimeSlot> availability;

        if(program.exists(ARG_PREFERRED_COURSES)){
            auto courses = program.get<std::vector<std::string>>(PREFERRED_COURSES);
            for (const auto& courseName : courses) {
                try {
                    Course course = rau.getCourse(courseName);
                    preferredCourses.push_back(course);
                } catch (const std::runtime_error& e) {
                    std::cerr << "Error: " << e.what() << " for course " << courseName << std::endl;
                }
            }
        }

        if(program.exists(ARG_AVAILABILITY)){
            auto availabilityArgs = program.get<std::vector<std::string>>(AVAILABILITY);
            for (size_t i = 0; i < availabilityArgs.size(); i += 3) {
                TimeSlot slot(availabilityArgs[i], availabilityArgs[i + 1],
                              availabilityArgs[i + 2]);
                availability.push_back(slot);
            }
        }

        Instructor instructor(instructorName, availability, preferredCourses);
        rau.addInstructor(instructor);

        rau.saveState(RESULT_JSON);

    } else if (program.exists(ARG_ADD_COURSE)) {
        auto courseName = program.get<std::string>(ADD_COURSE);
        std::vector<TimeSlot> preferredTimeSlots;

        if(program.exists(ARG_PREFERRED_TIME_SLOTS)){
            auto timeSlotArgs = program.get<std::vector<std::string>>(PREFERRED_TIME_SLOTS);
            for (size_t i = 0; i < timeSlotArgs.size(); i += 3) {
                TimeSlot slot(timeSlotArgs[i], timeSlotArgs[i + 1], timeSlotArgs[i + 2]);
                preferredTimeSlots.push_back(slot);
            }
        }

        Course course(courseName, preferredTimeSlots);
        rau.addCourse(course);

        rau.saveState(RESULT_JSON);

    } else if (program.exists(ARG_ADD_TIME_SLOT)) {
        auto timeSlotArgs = program.get<std::vector<std::string>>(ADD_TIMESLOT);
        std::string day = timeSlotArgs[0];
        std::string startTime = timeSlotArgs[1];
        std::string endTime = timeSlotArgs[2];
        TimeSlot timeSlot(day, startTime, endTime);
        rau.addTimeSlot(timeSlot);

        rau.saveState(RESULT_JSON);

    } else if (program.exists(ARG_SCHEDULE)) {
        auto schedule = rau.schedule();
        rau.saveState(RESULT_JSON);

        json universityData = rau.scheduleToJsonFormat();

        std::cout << universityData.dump(4) << std::endl;

    } else if (program.exists(ARG_CLEAR_FILE)) {
        std::ofstream file(RESULT_JSON, std::ofstream::trunc);
        if (file) {
            json emptyJson = json::object();
            file << emptyJson.dump(4);
            file.close();
            std::cout << "File cleared and initialized with an empty JSON object." << std::endl;
        } else {
            std::cerr << "Failed to open file " << RESULT_JSON << " for clearing." << std::endl;
        }

    } else if (program.exists(ARG_SHOW)) {
        json universityData;

        universityData[COURSES] = nlohmann::json::array();
        for (const auto& course : rau.getCourses()) {
            nlohmann::json courseData;
            courseData[COURSE_NAME] = course.getCourseName();
            universityData[COURSES].push_back(courseData);
        }

        universityData[INSTRUCTORS] = nlohmann::json::array();
        for (const auto& instructor : rau.getInstructors()) {
            nlohmann::json instructorData;
            instructorData[NAME] = instructor.getName();
            universityData[INSTRUCTORS].push_back(instructorData);
        }

        universityData[TIME_SLOTS] = nlohmann::json::array();
        for (const auto& slot : rau.getTimeSlots()) {
            nlohmann::json slotData;
            slotData[DAY] = slot.getDay();
            slotData[START_TIME] = slot.getStartTime();
            slotData[END_TIME] = slot.getEndTime();
            universityData[TIME_SLOTS].push_back(slotData);
        }

        std::cout << universityData.dump(4) << std::endl;
        rau.saveState(RESULT_JSON);

    }

    return 0;
}