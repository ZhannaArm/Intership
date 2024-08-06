#include <gtest/gtest.h>
#include "../include/TimeSlot.h"
#include "../include/Course.h"
#include "../include/Instructor.h"
#include "../include/University.h"

//test for method addCourse
TEST(UniversityTest, AddCourse) {
    University university;
    TimeSlot ts1("Monday", "12:50", "14:25");
    std::vector<TimeSlot> courseSlots = {ts1};
    Course course("Complex Analysis 203", courseSlots);

    university.addCourse(course);
    auto courses = university.getCourses();
    ASSERT_EQ(courses.size(), 1);
    ASSERT_EQ(courses[0].getCourseName(), "Complex Analysis 203");
}

//test for method addInstructor
TEST(UniversityTest, AddInstructor) {
    University university;
    TimeSlot ts1("Monday", "12:50", "14:25");
    std::vector<TimeSlot> availability = {ts1};
    std::vector<Course> preferredCourses;
    Instructor instructor("Berberyan S.L.", availability, preferredCourses);

    university.addInstructor(instructor);
    auto instructors = university.getInstructors();
    ASSERT_EQ(instructors.size(), 1);
    ASSERT_EQ(instructors[0].getName(), "Berberyan S.L.");
}

//test for method addTimeSlot
TEST(UniversityTest, AddTimeSlot) {
    University university;
    TimeSlot ts1("Monday", "12:50", "14:25");

    university.addTimeSlot(ts1);
    auto timeSlots = university.getTimeSlots();
    ASSERT_EQ(timeSlots.size(), 1);
    ASSERT_EQ(timeSlots[0].getDay(), "Monday");
    ASSERT_EQ(timeSlots[0].getStartTime(), "12:50");
    ASSERT_EQ(timeSlots[0].getEndTime(), "14:25");
}

//test for method saveState и loadState
TEST(UniversityTest, SaveLoadState) {
    University university;
    TimeSlot ts1("Monday", "12:50", "14:25");
    std::vector<TimeSlot> courseSlots = {ts1};
    Course course("Complex Analysis 203", courseSlots);
    std::vector<TimeSlot> availability = {ts1};
    std::vector<Course> preferredCourses = {course};
    Instructor instructor("Berberyan S.L.", availability, preferredCourses);

    university.addCourse(course);
    university.addInstructor(instructor);
    university.addTimeSlot(ts1);

    university.saveState("test_state.json");

    University loadedUniversity;
    loadedUniversity.loadState("test_state.json");

    auto courses = loadedUniversity.getCourses();
    auto instructors = loadedUniversity.getInstructors();
    auto timeSlots = loadedUniversity.getTimeSlots();

    ASSERT_EQ(courses.size(), 1);
    ASSERT_EQ(instructors.size(), 1);
    ASSERT_EQ(timeSlots.size(), 1);

    ASSERT_EQ(courses[0].getCourseName(), "Complex Analysis 203");
    ASSERT_EQ(instructors[0].getName(), "Berberyan S.L.");
    ASSERT_EQ(timeSlots[0].getDay(), "Monday");
}

//test for method schedule
TEST(UniversityTest, Schedule) {
    University university;

    TimeSlot ts1("Monday", "12:50", "14:25");
    TimeSlot ts2("Thursday", "9:00", "10:35");
    TimeSlot ts3("Wednesday", "10:45", "12:20");
    TimeSlot ts4("Friday", "9:00", "10:35");
    TimeSlot ts5("Friday", "12:50", "14:25");

    std::vector <TimeSlot> course1Slots = {ts3, ts4};
    Course course1("Complex Analysis 203", course1Slots);

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

    auto schedule = university.schedule();
    ASSERT_EQ(schedule.size(), 3);

    ASSERT_EQ(schedule[0].first.getCourseName(), "Complex Analysis 203");
    ASSERT_EQ(schedule[0].second.first.getDay(), "Friday");
    ASSERT_EQ(schedule[0].second.first.getStartTime(), "9:00");
    ASSERT_EQ(schedule[0].second.first.getEndTime(), "10:35");
    ASSERT_EQ(schedule[0].second.second.getName(), "Berberyan S.L.");

    ASSERT_EQ(schedule[1].first.getCourseName(), "Algorithms 203");
    ASSERT_EQ(schedule[1].second.first.getDay(), "Monday");
    ASSERT_EQ(schedule[1].second.first.getStartTime(), "12:50");
    ASSERT_EQ(schedule[1].second.first.getEndTime(), "14:25");
    ASSERT_EQ(schedule[1].second.second.getName(), "Hayrapetyan T.B.");

    ASSERT_EQ(schedule[2].first.getCourseName(), "Linux 203");
    ASSERT_EQ(schedule[2].second.first.getDay(), "Thursday");
    ASSERT_EQ(schedule[2].second.first.getStartTime(), "9:00");
    ASSERT_EQ(schedule[2].second.first.getEndTime(), "10:35");
    ASSERT_EQ(schedule[2].second.second.getName(), "Smbatyan M.A.");
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}