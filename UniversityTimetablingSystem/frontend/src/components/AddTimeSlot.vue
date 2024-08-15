<template>
  <div>
    <h1>Add Time Slots</h1>
    <div v-for="(timeSlot, index) in timeSlots" :key="index" class="time-slot-form">
      <input v-model="timeSlot.day" placeholder="Day" required />
      <input v-model="timeSlot.startTime" placeholder="Start Time" required />
      <input v-model="timeSlot.endTime" placeholder="End Time" required />
    </div>
    <button @click="addTimeSlot">Add Another Time Slot</button>
    <button @click="submitTimeSlots">Submit All Time Slots</button>
    <div v-if="message">
      <p :class="{'success-message': !isError, 'error-message': isError}">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      timeSlots: [
        { day: '', startTime: '', endTime: '' },
      ],
      message: '',
      isError: false
    };
  },
  methods: {
    addTimeSlot() {
      this.timeSlots.push({ day: '', startTime: '', endTime: '' });
    },
    submitTimeSlots() {
      const validTimeSlots = this.timeSlots.filter(slot => slot.day && slot.startTime && slot.endTime);
      if (validTimeSlots.length !== this.timeSlots.length) {
        alert('Please fill in all fields for each time slot.');
        return;
      }
      fetch('http://localhost:8000/api/add-time-slot/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ timeSlots: validTimeSlots }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'Time Slot(s) added successfully') {
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
    },
  },
}
</script>

<style>
.time-slot-form {
  margin-bottom: 20px;
}

.success-message {
  color: green;
  font-weight: bold;
}

.error-message {
  color: red;
  font-weight: bold;
}
</style>