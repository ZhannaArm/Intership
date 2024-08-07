#include "University.h"

void University::addCourse(const Course& course) { courses.push_back(course); }

void University::addInstructor(const Instructor& instructor) { instructors.push_back(instructor); }

void University::addTimeSlot(const TimeSlot& timeSlot) { timeSlots.push_back(timeSlot); }

std::vector<TimeSlot> University::getTimeSlots() const { return this->timeSlots; }

std::vector<Instructor> University::getInstructors() const { return this->instructors; }

std::vector<Course> University::getCourses() const { return this->courses; }

bool University::courseExists(const std::string& courseName) const {
    for (const auto& course : courses) {
        if (course.getCourseName() == courseName) {
            return true;
        }
    }
    return false;
}

Course University::getCourse(const std::string& courseName) const {
    for (const auto& course : courses) {
        if (course.getCourseName() == courseName) {
            return course;
        }
    }
    throw std::runtime_error("Course not found");
}

json University::convertCoursesToJson() const {
    json j = json::array();
    for (const auto& course : courses) {
        j.push_back(course.toJson());
    }
    return j;
}

json University::convertInstructorsToJson() const {
    json j = json::array();
    for (const auto& instructor : instructors) {
        j.push_back(instructor.toJson());
    }
    return j;
}

json University::convertTimeSlotsToJson() const {
    json j = json::array();
    for (const auto& timeSlot : timeSlots) {
        j.push_back(timeSlot.toJson());
    }
    return j;
}

void University::saveState(const std::string& filename) {
    json j;
<<<<<<< HEAD
    j[COURSES] = convertCoursesToJson();
    j[INSTRUCTORS] = convertInstructorsToJson();
    j[TIME_SLOTS] = convertTimeSlotsToJson();
=======
    j[COURSES] = json::array();
    for (const auto& course : courses) {
        j[COURSES].push_back(course.toJson());
    }

    j[INSTRUCTORS] = json::array();
    for (const auto& instructor : instructors) {
        j[INSTRUCTORS].push_back(instructor.toJson());
    }

    j[TIME_SLOTS] = json::array();
    for (const auto& timeSlot : timeSlots) {
        j[TIME_SLOTS].push_back(timeSlot.toJson());
    }
>>>>>>> 042574d (add Constants.h)

    std::ofstream file(filename);
    if (file.is_open()) {
        file << j.dump(4);
        file.close();
    } else {
        std::cerr << "Unable to open file for writing: " << filename << std::endl;
    }
}

void University::loadCoursesFromJson(const json& j) {
    courses.clear();
    for (const auto& courseJson : j[COURSES]) {
        std::string courseName = courseJson[COURSE_NAME];
        std::vector<TimeSlot> preferredTimeSlots;
        for (const auto& timeSlotJson : courseJson[PREFERRED_TIME_SLOTS]) {
            preferredTimeSlots.emplace_back(timeSlotJson[DAY], timeSlotJson[START_TIME],
                                            timeSlotJson[END_TIME]);
        }
        courses.emplace_back(courseName, preferredTimeSlots);
    }
}

void University::loadInstructorsFromJson(const json& j) {
    instructors.clear();
    for (const auto& instructorJson : j[INSTRUCTORS]) {
        std::string name = instructorJson[NAME];
        std::vector<TimeSlot> availability;
        for (const auto& timeSlotJson : instructorJson[AVAILABILITY]) {
            availability.emplace_back(timeSlotJson[DAY], timeSlotJson[START_TIME],
                                      timeSlotJson[END_TIME]);
        }
        std::vector<Course> preferredCourses;
        for (const auto& courseJson : instructorJson[PREFERRED_COURSES]) {
            std::string courseName = courseJson[COURSE_NAME];
            std::vector<TimeSlot> preferredTimeSlots;
            for (const auto& timeSlotJson : courseJson[PREFERRED_TIME_SLOTS]) {
                preferredTimeSlots.emplace_back(timeSlotJson[DAY], timeSlotJson[START_TIME],
                                                timeSlotJson[END_TIME]);
            }
            preferredCourses.emplace_back(courseName, preferredTimeSlots);
        }
        instructors.emplace_back(name, availability, preferredCourses);
    }
}

void University::loadTimeSlotsFromJson(const json& j) {
    timeSlots.clear();
    for (const auto& timeSlotJson : j[TIME_SLOTS]) {
        timeSlots.emplace_back(timeSlotJson[DAY], timeSlotJson[START_TIME],
                               timeSlotJson[END_TIME]);
    }
}

void University::loadState(const std::string& filename) {
    std::ifstream file(filename);
    if (file.is_open()) {
        json j;
        file >> j;

        loadCoursesFromJson(j);
        loadInstructorsFromJson(j);
        loadTimeSlotsFromJson(j);

        file.close();
    } else {
        std::cerr << "Unable to open file for reading: " << filename << std::endl;
    }
}

void University::displayInfo() const {
    std::cout << "University Information:" << std::endl;
    std::cout << "Courses:" << std::endl;
    for (const auto& course : courses) {
        course.displayInfo();
    }
    std::cout << std::endl;
    std::cout << "Instructors:" << std::endl;
    for (const auto& instructor : instructors) {
        instructor.displayInfo();
    }
    std::cout << std::endl;
    std::cout << "TimeSlots:" << std::endl;
    for (const auto& timeSlot : timeSlots) {
        timeSlot.displayInfo();
    }
    std::cout << std::endl;
}

// brute force algorithm for a large number of time slots, courses and instructors
void University::schedule_bruteForce() {
    for (const auto& course : courses) {
        bool scheduled = false;  // flag planned successfully planned course
        for (const auto& preferredTimeSlot :
             course.getPreferredTimeSlots()) {  // for each course we cover all preferred course
                                                // time slots
            for (const auto& instructor : instructors) {
                // we check if any of the teachers are available at this time and if the course is
                // on the teacher's list of preferred courses
                if (std::find(instructor.getAvailability().begin(),
                              instructor.getAvailability().end(),
                              preferredTimeSlot) != instructor.getAvailability().end() &&
                    std::find(instructor.getPreferredCourses().begin(),
                              instructor.getPreferredCourses().end(),
                              course) != instructor.getPreferredCourses().end()) {
                    if (scheduleMap.find(course) ==
                        scheduleMap
                            .end()) {  // if the course has not yet been added to the schedule
                        scheduleMap[course] = std::make_pair(instructor, preferredTimeSlot);
                        scheduled = true;
                        break;
                    }
                }
            }
            if (scheduled) {
                break;
            }
        }

        // assign a course to any available time slots if preferences are not met
        if (!scheduled) {
            for (const auto& timeSlot : timeSlots) {
                for (const auto& instructor : instructors) {
                    if (std::find(instructor.getAvailability().begin(),
                                  instructor.getAvailability().end(),
                                  timeSlot) != instructor.getAvailability().end()) {
                        if (scheduleMap.find(course) == scheduleMap.end()) {
                            scheduleMap[course] = scheduleMap[course] =
                                std::make_pair(instructor, timeSlot);
                            scheduled = true;
                            break;
                        }
                    }
                }
                if (scheduled) {
                    break;
                }
            }
        }
    }
}

// function to evaluate the cost of the current schedule (for simulated Annealing algorithm)
double University::calculateScheduleCost(
    const std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>>& schedule) {
    double cost = 0.0;
    for (const auto& entry : schedule) {
        const Course& course = entry.first;
        const TimeSlot& timeSlot = entry.second.first;
        const Instructor& instructor = entry.second.second;

        // hard constraints
        auto availability = instructor.getAvailability();
        if (std::find(availability.begin(), availability.end(), timeSlot) == availability.end()) {
            cost += 1000.0;  // high penalty if instructor is not available
        }
        auto preferredTimeSlots = course.getPreferredTimeSlots();
        // soft constraints
        if (std::find(preferredTimeSlots.begin(), preferredTimeSlots.end(), timeSlot) ==
            preferredTimeSlots.end()) {
            cost += 10.0;  // lower penalty if course is not in preferred time slot
        }

        auto preferredCourses = instructor.getPreferredCourses();
        if (std::find(preferredCourses.begin(), preferredCourses.end(), course) ==
            preferredCourses.end()) {
            cost += 10.0;  // lower penalty if instructor is not teaching preferred course
        }
    }
    return cost;
}

// Simulated Annealing algorithm to schedule courses
std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>> University::schedule() {
    // we initialize random seed
    std::srand(std::time(nullptr));

    // initial schedule (random assignment)
    std::vector<std::pair<Course, std::pair<TimeSlot, Instructor>>> currentSchedule;
    for (const auto& course : courses) {
        TimeSlot timeSlot = timeSlots[std::rand() % timeSlots.size()];
        Instructor instructor = instructors[std::rand() % instructors.size()];
        currentSchedule.emplace_back(course, std::make_pair(timeSlot, instructor));
    }

    // parameters for simulated annealing
    double temperature = 1200.0;  // temperature allows for many combinations
    double coolingRate =
        0.005;  // moderately low to give the algorithm enough time to find the optimal solution
    double minTemperature = 1.0;  // so that the algorithm terminates when the probability of making
                                  // worse decisions becomes very low

    auto bestSchedule = currentSchedule;
    double bestCost = calculateScheduleCost(bestSchedule);

    while (temperature > minTemperature) {
        // we create a new "candidate" schedule by making a small change to the current schedule
        auto newSchedule = currentSchedule;

        int randomIndex = std::rand() % newSchedule.size();
        TimeSlot newTimeSlot = timeSlots[std::rand() % timeSlots.size()];
        Instructor newInstructor = instructors[std::rand() % instructors.size()];
        newSchedule[randomIndex] = std::make_pair(newSchedule[randomIndex].first,
                                                  std::make_pair(newTimeSlot, newInstructor));

        // calculate the cost of the new schedule
        double currentCost = calculateScheduleCost(currentSchedule);
        double newCost = calculateScheduleCost(newSchedule);

        // decide whether to accept the new schedule(If the new schedule has a lower cost, it is
        // always accepted,
        //  otherwise the decision is made with a probability determined by the function
        //  std::exp...)
        if (newCost < currentCost ||
            std::exp((currentCost - newCost) / temperature) > (double)std::rand() / RAND_MAX) {
            currentSchedule = newSchedule;
        }

        // update the best schedule if the new schedule is better
        if (newCost < bestCost) {
            bestSchedule = newSchedule;
            bestCost = newCost;
        }

        // cool down the temperature
        temperature *= 1 - coolingRate;
    }

    Schedule = bestSchedule;
    return bestSchedule;  // I do this for google tests
}

std::vector<std::tuple<std::string, std::string, std::string>> University::scheduleToJsonFormat()
    const {
    std::vector<std::tuple<std::string, std::string, std::string>> result;
    for (const auto& entry : Schedule) {
        std::string courseName = entry.first.getCourseName();
        std::string timeSlot = entry.second.first.getDay() + " " +
                               entry.second.first.getStartTime() + "-" +
                               entry.second.first.getEndTime();
        std::string instructorName = entry.second.second.getName();
        result.emplace_back(courseName, timeSlot, instructorName);
    }
    return result;
}

void University::displaySchedule() const {
    std::cout << "SCHEDULE:" << std::endl;
    for (const auto& entry : Schedule) {
        std::cout << "Course: " << entry.first.getCourseName()
                  << ", Time Slot: " << entry.second.first.getDay() << " "
                  << entry.second.first.getStartTime() << "-" << entry.second.first.getEndTime()
                  << ", Instructor: " << entry.second.second.getName() << std::endl;
    }
}

// for brute force algorithm
void University::displayScheduleMap() const {
    std::cout << "Schedule:" << std::endl;
    for (const auto& entry : scheduleMap) {
        std::cout << "Course: " << entry.first.getCourseName()
                  << " | Instructor: " << entry.second.first.getName() << " | TimeSlot: ";
        entry.second.second.displayInfo();
    }
}
