<template>
  <div>
    <h1>University Details</h1>
    <button @click="showUniversityDetails">Show University Details</button>
    <div v-if="university">
      <h2>Courses</h2>
      <ul>
        <li v-for="course in university.courses" :key="course.courseName">{{ course.courseName }}</li>
      </ul>
      <h2>Instructors</h2>
      <ul>
        <li v-for="instructor in university.instructors" :key="instructor.name">{{ instructor.name }}</li>
      </ul>
      <h2>Time Slots</h2>
      <ul>
        <li v-for="slot in university.timeSlots" :key="slot.day + slot.startTime">{{ slot.day }} {{ slot.startTime }} - {{ slot.endTime }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      university: null,
    };
  },
  methods: {
    showUniversityDetails() {
      fetch('http://localhost:8000/api/show-university/')
        .then(response => response.json())
        .then(data => {
          this.university = data;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
  },
}
</script>
