<template>
  <div id="app">
    <AddInstructor />
    <AddCourse />
    <AddTimeSlot />
    <CreateSchedule />
    <ShowDetails />
  </div>
</template>

<script>
import AddInstructor from './components/AddInstructor.vue';
import AddCourse from './components/AddCourse.vue';
import AddTimeSlot from './components/AddTimeSlot.vue';
import CreateSchedule from './components/CreateSchedule.vue';
import ShowDetails from './components/ShowDetails.vue';

export default {
  name: 'App',
  components: {
    AddInstructor,
    AddCourse,
    AddTimeSlot,
    CreateSchedule,
    ShowDetails
  }
};
</script>
