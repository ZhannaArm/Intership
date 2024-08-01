#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "University.h"
#include "Course.h"
#include "Instructor.h"
#include "TimeSlot.h"

namespace py = pybind11;

PYBIND11_MODULE(university_bindings, m) {
    py::class_<University>(m, "University")
        .def(py::init<>())
        .def("addInstructor", &University::addInstructor)
        .def("addCourse", &University::addCourse)
        .def("addTimeSlot", &University::addTimeSlot)
        .def("schedule", &University::schedule)
        .def("displayInfo", &University::displayInfo)
        .def("saveState", &University::saveState)
        .def("loadState", &University::loadState)
        .def("courseExists", &University::courseExists)
        .def("getCourse", &University::getCourse)
        .def("getCourses", &University::getCourses)
        .def("getInstructors", &University::getInstructors)
        .def("getTimeSlots", &University::getTimeSlots)
        .def("scheduleToJsonFormat", &University::scheduleToJsonFormat);

    py::class_<Course>(m, "Course")
        .def(py::init<const std::string&, const std::vector<TimeSlot>&>())
        .def("getCourseName", &Course::getCourseName)
        .def("getPreferredTimeSlots", &Course::getPreferredTimeSlots);

    py::class_<Instructor>(m, "Instructor")
        .def(py::init<const std::string&, const std::vector<TimeSlot>&, const std::vector<Course>&>())
        .def("getName", &Instructor::getName)
        .def("getAvailability", &Instructor::getAvailability)
        .def("getPreferredCourses", &Instructor::getPreferredCourses);

    py::class_<TimeSlot>(m, "TimeSlot")
        .def(py::init<const std::string&, const std::string&, const std::string&>())
        .def("getDay", &TimeSlot::getDay)
        .def("getStartTime", &TimeSlot::getStartTime)
        .def("getEndTime", &TimeSlot::getEndTime);
}
