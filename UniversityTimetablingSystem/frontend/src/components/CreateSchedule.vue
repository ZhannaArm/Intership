<template>
  <div>
    <h1>Create Schedule</h1>
    <button @click="createSchedule">Create Schedule</button>
    <div v-if="schedule">
      <h2>Schedule</h2>
      <ul>
        <li v-for="entry in schedule" :key="entry.course">
          Course: {{ entry.course }}, Time Slot: {{ entry.timeSlot }}, Instructor: {{ entry.instructor }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      schedule: null,
    };
  },
  methods: {
    createSchedule() {
      fetch('http://localhost:8000/api/schedule/', {
        method: 'POST',
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        this.schedule = data.schedule;
        console.log('Schedule created:', this.schedule);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    },
  },
}
</script>