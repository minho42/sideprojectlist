<template>
  <nav id="navbar">
  <header class="bg-white border-b border-gray-300 shadow-sm">
    <div class="flex items-center justify-between pl-3 py-2 h-16">
      <div class="flex items-center">
        <NuxtLink to="/" class=" px-1 py-1 font-bold text-lg">
          Side Project List
        </NuxtLink>
      </div>
      <div class="mr-3" style="touch-action: manipulation;">
        <NuxtLink to="/about"
        class="block px-3 py-2 ml-2 text-center rounded-lg border-none hover:bg-gray-200">
        About</NuxtLink>
      </div>
    </div>
  </header>
</nav>
</template>

<script>
export default {
  name: "Navbar",
  data() {
  return {
  }
  }
};
</script>

<style></style>
