#include <vector>
#include "TimeSlot.h"
#include "Course.h"
#include "Instructor.h"
#include "University.h"

int main() {
    University university;

    TimeSlot ts1("Monday", "12:50", "14:25");
    TimeSlot ts2("Thursday", "9:00", "10:35");
    TimeSlot ts3("Wednesday", "10:45", "12:20");
    TimeSlot ts4("Friday", "9:00", "10:35");
    TimeSlot ts5("Friday", "12:50", "14:25");

    std::vector <TimeSlot> course1Slots = {ts3, ts4};
    Course course1("Сomplex analysis 203", course1Slots);

    std::vector <TimeSlot> course2Slots = {ts1};
    Course course2("Algorithms 203", course2Slots);

    std::vector <TimeSlot> course3Slots = {ts2};
    Course course3("Linux 203", course3Slots);

    university.addCourse(course1);
    university.addCourse(course2);
    university.addCourse(course3);

    std::vector <TimeSlot> instructor1Availability = {ts1, ts4};
    std::vector <TimeSlot> instructor2Availability = {ts1, ts5};
    std::vector <TimeSlot> instructor3Availability = {ts2};
    std::vector <Course> instructor1PreferredCourses = {course1};
    std::vector <Course> instructor2PreferredCourses = {course2};
    std::vector <Course> instructor3PreferredCourses = {course3};
    Instructor instructor1("Berberyan S.L.", instructor1Availability, instructor1PreferredCourses);
    Instructor instructor2("Hayrapetyan T.B.", instructor2Availability, instructor2PreferredCourses);
    Instructor instructor3("Smbatyan M.A.", instructor3Availability, instructor3PreferredCourses);

    university.addInstructor(instructor1);
    university.addInstructor(instructor2);
    university.addInstructor(instructor3);
    university.addTimeSlot(ts1);
    university.addTimeSlot(ts2);
    university.addTimeSlot(ts3);
    university.addTimeSlot(ts4);
    university.addTimeSlot(ts5);

    //university.displayInfo(); //function to see all information about the university
    university.saveState("rau_state.json");
    university.loadState("rau_state.json");
    auto schedule = university.schedule();
    university.displaySchedule();
    return 0;
}
