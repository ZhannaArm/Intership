#include <iostream>
#include <vector>
#include <cstdio>

#include "Course.h"
#include "Instructor.h"
#include "TimeSlot.h"
#include "University.h"
#include "argparse.h"

void processArgs(int argc, char** argv, University& university) {
    std::string stateFile = "result.json";

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];

        if (arg == "--stateFile" && i + 1 < argc) {
            stateFile = argv[++i];
        } else if (arg == "--addInstructor" && i + 1 < argc) {
            university.loadState(stateFile);
            std::string instructorJson = argv[++i];
            json j = json::parse(instructorJson);
            std::vector<Course> preferredCourses;
            std::vector<TimeSlot> availability;

            std::string instructorName = j["name"];
            for (const auto& courseJson : j["preferred_courses"]) {
                std::string courseName = courseJson["courseName"];
                try {
                    Course course = university.getCourse(courseName);
                    preferredCourses.push_back(course);
                } catch (const std::runtime_error& e) {
                    std::cerr << "Error: " << e.what() << " for course " << courseName << std::endl;
                }
            }

            for (const auto& slot : j["availability"]) {
                TimeSlot timeSlot(slot["day"], slot["startTime"], slot["endTime"]);
                availability.push_back(timeSlot);
            }

            Instructor instructor(instructorName, availability, preferredCourses);
            university.addInstructor(instructor);
            university.saveState(stateFile);

        } else if (arg == "--addCourse" && i + 1 < argc) {
            university.loadState(stateFile);
            std::string courseJson = argv[++i];
            json j = json::parse(courseJson);

            std::string courseName = j["name"];
            std::vector<TimeSlot> preferredTimeSlots;
            for (const auto& ts : j["preferred_time_slots"]) {
                TimeSlot timeSlot(ts["day"], ts["startTime"], ts["endTime"]);
                preferredTimeSlots.push_back(timeSlot);
            }

            Course course(courseName, preferredTimeSlots);
            std::cout << "COURSE: ";
            course.displayInfo();
            university.addCourse(course);
            university.saveState(stateFile);

        } else if (arg == "--addTimeSlot" && i + 1 < argc) {
            university.loadState(stateFile);
            std::string timeSlotArg = argv[++i];
            json timeSlotJson = json::parse(timeSlotArg);

            for (const auto& slot : timeSlotJson) {
                TimeSlot timeSlot(slot["day"], slot["startTime"], slot["endTime"]);
                university.addTimeSlot(timeSlot);
            }
            university.saveState(stateFile);

        } else if (arg == "--schedule") {
            university.loadState(stateFile);
            auto schedule = university.schedule();
            university.saveState(stateFile);

            university.displaySchedule();

        } else if (arg == "--clearFile") {
            std::ofstream file(stateFile, std::ofstream::trunc);
            if (file) {
                json emptyJson = json::object();
                file << emptyJson.dump(4);
                file.close();
                std::cout << "File cleared and initialized with an empty JSON object." << std::endl;
            } else {
                std::cerr << "Failed to open file " << stateFile << " for clearing." << std::endl;
            }

        } else {
            std::cerr << "Unknown argument: " << arg << std::endl;
        }
    }

    if (stateFile != "result.json" || std::find(argv, argv + argc, "--clearFile") == argv + argc) {
        university.loadState(stateFile);
    }
}

int main(int argc, char** argv) {
    University university;

    processArgs(argc, argv, university);
    return 0;
}