<template>
  <div class="text-gray-800 text-lg">
    <Navbar />
    <Nuxt />
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
export default {
  components: {
    Navbar,
  },
}
</script>

<style>
body{
  background-color: #f0f2f5;
}
</style>
