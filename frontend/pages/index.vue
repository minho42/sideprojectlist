<template>
  <div id="app">
    <ProjectList :projectData="projectData" :isLoading="isLoading" />
  </div>
</template>

<script>
import ProjectList from "../components/ProjectList.vue";
import axios from "axios";

export default {
  name: "App",
  components: {
    ProjectList,
  },
  data() {
    return {
      isLoading: true,
      isErrored: false,
      projectData: []
    };
  },
  created() {
    axios
      .get("data.json")
      .then((response) => (this.projectData = response.data))
      .catch((error) => {
        console.log(error)
        this.isErrored = true
        }
      )
      .finally(()=> this.isLoading=false)
  },
};
</script>

<style>
</style>
