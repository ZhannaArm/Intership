<template>
  <div>
    <h1>Add Instructor</h1>
    <div v-for="(instructor, index) in instructors" :key="index" class="instructor-form">
      <input v-model="instructor.name" placeholder="Instructor Name" required />
      <div v-for="(course, courseIndex) in instructor.preferredCourses" :key="courseIndex">
        <input v-model="instructor.preferredCourses[courseIndex].courseName" placeholder="Preferred Course" />
      </div>
      <button @click="addPreferredCourse(index)">Add Preferred Course</button>
      <div v-for="(slot, slotIndex) in instructor.availability" :key="slotIndex">
        <input v-model="instructor.availability[slotIndex].day" placeholder="Day" />
        <input v-model="instructor.availability[slotIndex].startTime" placeholder="Start Time" />
        <input v-model="instructor.availability[slotIndex].endTime" placeholder="End Time" />
      </div>
      <button @click="addPreferredTimeSlot(index)">Add Preferred Time Slot</button>
    </div>
    <button @click="addInstructor">Add Another Instructor</button>
    <button @click="submitInstructors">Submit All Instructors</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      instructors: [
        {
          name: '',
          preferredCourses: [
            {
              courseName: '',
              preferredTimeSlots: [{ day: '', startTime: '', endTime: '' }],
            },
          ],
          availability: [{ day: '', startTime: '', endTime: '' }],
        },
      ],
    };
  },
  methods: {
    addPreferredCourse(index) {
      this.instructors[index].preferredCourses.push({
        courseName: '',
        preferredTimeSlots: [{ day: '', startTime: '', endTime: '' }],
      });
    },
    addPreferredTimeSlot(index) {
      this.instructors[index].availability.push({ day: '', startTime: '', endTime: '' });
    },
    addInstructor() {
      this.instructors.push({
        name: '',
        preferredCourses: [
          {
            courseName: '',
            preferredTimeSlots: [{ day: '', startTime: '', endTime: '' }],
          },
        ],
        availability: [{ day: '', startTime: '', endTime: '' }],
      });
    },
    submitInstructors() {
      this.instructors.forEach(instructor => {
        const data = {
          name: instructor.name,
          preferred_courses: instructor.preferredCourses.map(course => ({
            courseName: course.courseName,
            preferredTimeSlots: course.preferredTimeSlots
          })),
          availability: instructor.availability,
        };
        fetch('http://localhost:8000/api/add-instructor/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'Error') {
            console.error('Error:', data.message);
          } else {
            console.log('Success:', data);
          }
        })
        .catch((error) => {
          console.error('Error:', error);
        });
      });
    },
  },
}
</script>

<style>
.instructor-form {
  margin-bottom: 20px;
}
</style>
