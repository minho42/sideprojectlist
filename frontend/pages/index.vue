<template>
  <div id="app">
    <ProjectList :projectData="projectData" />
  </div>
</template>

<script>
import projectData from '../data.json'
import ProjectList from "../components/ProjectList.vue";

export default {
  name: "App",
  components: {
    ProjectList,
  },
  data() {
    return {
      projectData
    };
  },
};
</script>
