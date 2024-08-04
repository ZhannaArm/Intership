#include <iostream>
#include <vector>

#include "Course.h"
#include "Instructor.h"
#include "TimeSlot.h"
#include "University.h"
#include "argparse.h"
#include "Constants.h"

// function to find a course by name in the university
Course* findCourseByName(const std::string& courseName, University& university) {
    for (Course& course : university.getCourses()) {
        if (course.getCourseName() == courseName) {
            return &course;
        }
    }
    return nullptr;
}

int main(int argc, char** argv) {
    argparse::ArgumentParser program("UniversityTimetablingSystem", "University");

    program.add_argument(ARG_ADD_INSTRUCTOR, "Add a new instructor", false);

    program.add_argument(ARG_ADD_COURSE, "Add a new course", false);

    program.add_argument(ARG_ADD_TIME_SLOT, "Add a new time slot", false);

    program.add_argument(ARG_SCHEDULE, "Generate the schedule", false);

    program.add_argument(ARG_AVAILABILITY, "Represents instructor's availability", false);

    program.add_argument(ARG_PREFERRED_COURSES, "Represents instructor's preferred courses", false);

    program.add_argument(ARG_PREFERRED_TIME_SLOTS, "Represents preferred course time slots", false);

    program.add_argument(ARG_CLEAR_FILE, "Clear the result.json file", false);

    program.add_argument(ARG_STATE_FILE, "Path to the state file (e.g., result.json)", true);

    // parse arguments
    auto result = program.parse(argc, const_cast<const char**>(argv));
    if (result) {
        std::cerr << "Error: " << result.what() << std::endl;
        program.print_help();
        return 1;
    }
    std::string state_file = program.get<std::string>(ARG_STATE_FILE);
    University rau;
    rau.loadState(state_file);

    if (program.exists(ARG_ADD_INSTRUCTOR)) {
        std::string instructorName = program.get<std::string>(ADD_INSTRUCTOR);
        std::vector<Course> preferredCourses;
        std::vector<TimeSlot> availability;

        if (program.exists(ARG_PREFERRED_COURSES)) {
            auto courses = program.get<std::vector<std::string>>(PREFERRED_COURSES);
            for (const auto& courseName : courses) {
                Course* course = findCourseByName(courseName, rau);
                if (course != nullptr) {
                    preferredCourses.push_back(*course);
                } else {
                    std::cerr << "Course " << courseName << " not found!" << std::endl;
                }
            }
        }

        if (program.exists(ARG_AVAILABILITY)) {
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
    }

    if (program.exists(ARG_ADD_COURSE)) {
        std::string courseName = program.get<std::string>(ADD_COURSE);
        std::vector<TimeSlot> preferredTimeSlots;

        if (program.exists(ARG_PREFERRED_TIME_SLOTS)) {
            auto timeSlotArgs = program.get<std::vector<std::string>>(PREFERRED_TIME_SLOTS);
            for (size_t i = 0; i < timeSlotArgs.size(); i += 3) {
                TimeSlot slot(timeSlotArgs[i], timeSlotArgs[i + 1], timeSlotArgs[i + 2]);
                preferredTimeSlots.push_back(slot);
            }
        }

        Course course(courseName, preferredTimeSlots);
        rau.addCourse(course);

        rau.saveState(RESULT_JSON);
    }

    if (program.exists(ARG_ADD_TIME_SLOT)) {
        auto timeSlotArgs = program.get<std::vector<std::string>>(ADD_TIMESLOT);
        std::string day = timeSlotArgs[0];
        std::string startTime = timeSlotArgs[1];
        std::string endTime = timeSlotArgs[2];

        TimeSlot timeSlot(day, startTime, endTime);
        rau.addTimeSlot(timeSlot);

        rau.saveState(RESULT_JSON);
    }

    if (program.exists(ARG_SCHEDULE)) {
        rau.loadState(RESULT_JSON);
        auto schedule = rau.schedule();
        rau.displaySchedule();
        std::cout << "Schedule generated!" << std::endl;
        return 0;
    }

    if (program.exists(ARG_CLEAR_FILE)) {
        std::ofstream file(RESULT_JSON,
                           std::ofstream::trunc);  // we open the file in cleaning mode
        if (!file) {
            std::cerr << "Failed to open file result.json for clearing." << std::endl;
        }

        json emptyJson = json::object();
        file << emptyJson.dump(4);

        file.close();
        std::cout << "File result.json has been cleared and initialized with an empty JSON object."
                  << std::endl;
        rau.loadState(RESULT_JSON);
    }

    rau.displayInfo();
    return 0;
}