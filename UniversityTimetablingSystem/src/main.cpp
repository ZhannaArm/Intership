#include <iostream>
#include <vector>
#include "argparse.h"
#include "TimeSlot.h"
#include "Course.h"
#include "Instructor.h"
#include "University.h"

//function to find a course by name in the university
Course* findCourseByName(const std::string& courseName, University& university) {
    for (Course& course : university.getCourses()) {
        if (course.getCourseName() == courseName) {
            return &course;
        }
    }
    return nullptr;
}

int main(int argc, char **argv) {
    argparse::ArgumentParser program("UniversityTimetablingSystem", "University");

    program.add_argument("--addInstructor", "Add a new instructor", false);

    program.add_argument("--addCourse", "Add a new course", false);

    program.add_argument("--addTimeSlot", "Add a new time slot", false);

    program.add_argument("--schedule", "Generate the schedule", false);

    program.add_argument("--availability", "Represents instructor's availability", false);

    program.add_argument("--preferredCourses", "Represents instructor's preferred courses", false);

    program.add_argument("--preferredTimeSlots", "Represents preferred course time slots", false);

    program.add_argument("--clearFile", "Clear the result.json file", false);

    program.add_argument("--stateFile", "Path to the state file (e.g., result.json)", true);

    //parse arguments
    auto result = program.parse(argc, const_cast<const char**>(argv));
    if (result) {
        std::cerr << "Error: " << result.what() << std::endl;
        program.print_help();
        return 1;
    }
    std::string state_file = program.get<std::string>("--stateFile");
    University rau;
    rau.loadState(state_file);

    if (program.exists("--addInstructor")) {
        std::string instructorName = program.get<std::string>("addInstructor");
        std::vector<Course> preferredCourses;
        std::vector<TimeSlot> availability;

        if (program.exists("--preferredCourses")) {
            auto courses = program.get<std::vector<std::string>>("preferredCourses");
            for (const auto& courseName : courses) {
                Course* course = findCourseByName(courseName, rau);
                if (course != nullptr) {
                    preferredCourses.push_back(*course);
                } else {
                    std::cerr << "Course " << courseName << " not found!" << std::endl;
                }
            }
        }

        if (program.exists("--availability")) {
            auto availabilityArgs = program.get<std::vector<std::string>>("availability");
            for (size_t i = 0; i < availabilityArgs.size(); i += 3) {
                TimeSlot slot(availabilityArgs[i], availabilityArgs[i+1], availabilityArgs[i+2]);
                availability.push_back(slot);
            }
        }

        Instructor instructor(instructorName, availability, preferredCourses);
        rau.addInstructor(instructor);

        rau.saveState("result.json");
    }

    if (program.exists("--addCourse")) {
        std::string courseName = program.get<std::string>("addCourse");
        std::vector<TimeSlot> preferredTimeSlots;

        if (program.exists("--preferredTimeSlots")) {
            auto timeSlotArgs = program.get<std::vector<std::string>>("preferredTimeSlots");
            for (size_t i = 0; i < timeSlotArgs.size(); i += 3) {
                TimeSlot slot(timeSlotArgs[i], timeSlotArgs[i+1], timeSlotArgs[i+2]);
                preferredTimeSlots.push_back(slot);
            }
        }

        Course course(courseName, preferredTimeSlots);
        rau.addCourse(course);

        rau.saveState("result.json");
    }

    if (program.exists("--addTimeSlot")) {
        auto timeSlotArgs = program.get<std::vector<std::string>>("addTimeSlot");
        std::string day = timeSlotArgs[0];
        std::string startTime = timeSlotArgs[1];
        std::string endTime = timeSlotArgs[2];

        TimeSlot timeSlot(day, startTime, endTime);
        rau.addTimeSlot(timeSlot);

        rau.saveState("result.json");
    }

    if (program.exists("--schedule")) {
        rau.loadState("result.json");
        auto schedule = rau.schedule();
        rau.displaySchedule();
        std::cout << "Schedule generated!" << std::endl;
        return 0;
    }

    if(program.exists("--clearFile")){
        std::ofstream file("result.json", std::ofstream::trunc); //we open the file in cleaning mode
        if (!file) {
            std::cerr << "Failed to open file result.json for clearing." << std::endl;
        }

        json emptyJson = json::object();
        file << emptyJson.dump(4);

        file.close();
        std::cout << "File result.json has been cleared and initialized with an empty JSON object." << std::endl;
        rau.loadState("result.json");
    }

    rau.displayInfo();
    return 0;
}