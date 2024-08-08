<template>
  <div>
    <h1>Add Courses</h1>
    <div v-for="(course, index) in courses" :key="index" class="course-form">
      <input v-model="course.courseName" placeholder="Course Name" required />
      <div v-for="(timeSlot, slotIndex) in course.preferredTimeSlots" :key="slotIndex">
        <input v-model="course.preferredTimeSlots[slotIndex].day" placeholder="Day" />
        <input v-model="course.preferredTimeSlots[slotIndex].startTime" placeholder="Start Time" />
        <input v-model="course.preferredTimeSlots[slotIndex].endTime" placeholder="End Time" />
      </div>
      <button @click="addPreferredTimeSlot(index)">Add Preferred Time Slot</button>
    </div>
    <button @click="addCourse">Add Another Course</button>
    <button @click="submitCourses">Submit All Courses</button>
    <div v-if="message">
      <p :class="{ 'error-message': isError }">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      courses: [
        {
          courseName: '',
          preferredTimeSlots: [{ day: '', startTime: '', endTime: '' }],
        },
      ],
      message: '',
      isError: false
    };
  },
  methods: {
    addPreferredTimeSlot(index) {
      this.courses[index].preferredTimeSlots.push({ day: '', startTime: '', endTime: '' });
    },
    addCourse() {
      this.courses.push({
        courseName: '',
        preferredTimeSlots: [{ day: '', startTime: '', endTime: '' }],
      });
    },
    submitCourses() {
      this.courses.forEach(course => {
        const data = {
          courseName: course.courseName,
          preferredTimeSlots: course.preferredTimeSlots,
        };
        fetch('http://localhost:8000/api/add-course/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'Course added successfully') {
            this.message = data.status;
            this.isError = false;
          } else {
            this.message = data.message || 'An error occurred';
            this.isError = true;
          }
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
          this.message = 'An error occurred';
          this.isError = true;
        });
      });
    },
  },
}
</script>

<style>
.course-form {
  margin-bottom: 20px;
}
</style>
