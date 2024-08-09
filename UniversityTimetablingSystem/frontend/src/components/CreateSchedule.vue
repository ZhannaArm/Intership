<template>
  <div>
    <h1>Create Schedule</h1>
    <button @click="createSchedule">Create Schedule</button>
    <div v-if="schedule">
      <h2>Schedule</h2>
      <ul>
        <li v-for="(entry, index) in schedule" :key="index">
          Course: {{ entry[0] }}, Time Slot: {{ entry[1] }}, Instructor: {{ entry[2] }}
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
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.schedule) {
          this.schedule = data.schedule;
          console.log('Schedule created:', this.schedule);
        } else {
          console.error('No schedule data available');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    },
  },
}
</script>