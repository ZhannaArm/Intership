# University Timetabling System

## Project Description

This project is designed to create a timetable for university courses, assigning instructors to each course based on their availability and preferences. The project includes classes to represent courses, instructors, and time slots, as well as an algorithm to generate the timetable.

## Class Structure

### Classes
- **TimeSlot**: Represents a time slot for scheduling courses.
- **Course**: Represents a course that needs to be scheduled.
- **Instructor**: Represents an instructor who can teach courses and has specific availability.
- **University**: Represents the combination of courses, instructors, and time slots.

### Attributes

- **TimeSlot**: `day` (string), `startTime` (string), `endTime` (string)
- **Course**: `courseName` (string), `preferredTimeSlots` (list of TimeSlot objects)
- **Instructor**: `name` (string), `availability` (list of TimeSlot objects), `preferredCourses` (list of Course objects)
- **University**: `courses` (list of Course objects), `instructors` (list of Instructor objects), `timeSlots` (list of TimeSlot objects)

### Methods

- **TimeSlot**
    - `displayInfo()`: Prints time slot information.
- **Course**
    - `displayInfo()`: Prints course information.
- **Instructor**
    - `displayInfo()`: Prints instructor information.
- **University**
    - `addCourse(course: Course)`: Adds a course to the university.
    - `addInstructor(instructor: Instructor)`: Adds an instructor to the university.
    - `addTimeSlot(timeSlot: TimeSlot)`: Adds a time slot to the university.
    - `saveState()`: Saves the current state of the university to a file in JSON format.
    - `loadState()`: Loads the state of the university from a file in JSON format.
    - `schedule()`: Returns a timetable that satisfies all hard constraints and as many soft constraints as possible.

### Constraints

#### Hard Constraints
1. Each course must be scheduled exactly once in an available time slot and assigned to an instructor.
2. An instructor can only be assigned to a course if they are available during the corresponding time slot.
3. An instructor cannot be scheduled to teach more than one course at the same time.

#### Soft Constraints
1. Courses should be scheduled in preferred time slots if possible.
2. Instructors should be assigned to their preferred courses if possible.

## Usage

### Building the Project

To build the project, you need to have CMake installed. Run the provided `build.sh` script. This script supports three modes: `build`, `release`, and `debug`.

```sh
git submodule update --init --recursive
./build.sh # Build the project (default to Release mode)
./build.sh release # Build the project in Release mode
./build.sh debug   # Build the project in Debug mode
```
###Running the Project
The project provides several commands to manage instructors, courses, and time slots, as well as to generate the schedule.

#### **If you want to work with the program through the terminal, you can follow these steps:**
#### Commands
- **Add Time SLot**: Adds a time slot(day, start time, end time).
  ```sh
  ./UniversityTimetablingSystem --addTimeSlot --day DAY --startTime START --endTime END
  ```
- **Add Course**: Adds a course with its preferred time slots.
  ```sh
  ./UniversityTimetablingSystem --addCourse NAME --preferredTimeSlots DAY1 START1 END1
  DAY2 START_TIME1 END_TIME2 ...
  ```
- **Add Instructor**: Adds an instructor with their preferred courses and availability.
  ```sh
  ./UniversityTimetablingSystem --addInstructor NAME --preferredCourses COURSE1 COURSE2 ... 
  --availability DAY1 START1 END1 DAY2 START2 END2 ...
  ```
- **Generate schedule**: Generates the schedule based on the added data and prints it to the console.
  ```sh
  ./UniversityTimetablingSystem --schedule
  ```

####**If you want to work with the program over the network, open two terminals and write this in one of them:**
  ```sh
  cd your-repository
  chmod +x run-server.sh #This only needs to be done once
  chmod +x run-frontend.sh #This only needs to be done once
  ./run-server.sh
  ```
And in the other this:
  ```sh
  cd your-repository
  ./run-frontend.sh
  ```
###IMPORTANT
You must add courses **BEFORE** you add instructors.

####EXAMPLE with running the project through the terminal
```sh
./run/UniversityTimetablingSystem --addTimeSlot Monday 11:00 14:00
./run/UniversityTimetablingSystem --addTimeSlot Wednesday 14:00 16:00
./run/UniversityTimetablingSystem --addTimeSlot Tuesday 11:00 13:00
./run/UniversityTimetablingSystem --addCourse Mathematics --preferredTimeSlots Tuesday 11:00 13:00
./run/UniversityTimetablingSystem --addCourse History --preferredTimeSlots Monday 10:00 12:00 Wednesday 13:00 15:00
./run/UniversityTimetablingSystem --addCourse Physics --preferredTimeSlots Wednesday 14:00 16:00 Monday 11:00 14:00
./run/UniversityTimetablingSystem --addInstructor James --preferredCourses Mathematics Physics
     --availability Monday 09:00 12:00 Wednesday 14:00 16:00 Tuesday 11:00 13:00
./run/UniversityTimetablingSystem --addInstructor Sara --preferredCourses History --availability Monday 10:00 12:00
     Wednesday 14:00 16:00 Friday 11:00 14:00
./run/UniversityTimetablingSystem --schedule
```