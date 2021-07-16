<template>
  <div
    class="flex flex-col items-center justify-start sm:w-1/2 md:w-1/3 lg:w-1/4"
  >
    <div
      class="border border-gray-500 mx-1 sm:mx-2 my-4 sm:my-3 bg-white rounded-xl shadow-lg"
    >
      <div class="border-b border-gray-400 ">
        <a
          :href="link"
          target="_blank"
          rel="noopener noreferrer"
          class="flex flex-col items-center justify-center hover:bg-gray-300 "
        >
          <img
            class="w-full rounded-t-xl"
            :src="screenshot_url"
            alt="screenshot"
          />
        </a>
      </div>

      <div class="px-4 py-2">
        <div class="flex items-center justify-start flex-wrap">
          <div class="flex-shrink-0">
            <img
              v-if="avatar_url"
              class="w-8 rounded-full mr-1"
              :src="avatar_url"
              alt="twitter avatar"
            />
            <!-- user-circle -->
            <svg
              v-if="!avatar_url"
              class="w-8 mr-1 text-gray-400"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z"
                clipRule="evenodd"
              />
            </svg>
          </div>

          <div class="text-2xl font-bold">
            {{ fullname }}
          </div>
        </div>

        <div class="mt-1 mb-1">
          <div class="flex flex-wrap items-center mt-2">
            <div
              @click="$emit('setSelectedTag', tag)"
              v-for="tag in tags"
              :key="tag"
              class="block bg-gray-300 hover:bg-gray-400 cursor-pointer rounded-lg px-2 mr-2 mt-2"
              :class="
                selectedTag === tag
                  ? 'bg-green-300 hover:bg-green-300'
                  : 'bg-gray-300 hover:bg-gray-400'
              "
            >
              {{ tag }}
            </div>
          </div>

          <div class="flex flex-wrap items-center justify-center mt-4">
            <div v-if="twitter_handle" class="">
              <a
                :href="twitterUrl"
                class="flex items-center text-sm text-gray-700 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <!-- <svg class="w-5 h-5" fill="currentColor" role="img" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><title>Twitter icon</title><path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"></path></svg> -->
                Twitter
              </a>
            </div>
            <div v-if="github_handle" class="ml-4">
              <a
                :href="githubUrl"
                class="flex items-center text-sm text-gray-700 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <!-- <svg class="w-5 h-5" fill="currentColor" role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><title>GitHub icon</title><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"></path></svg> -->
                Github
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProjectItem",
  props: {
    slug: String,
    link: String,
    fullname: String,
    twitter_handle: String,
    github_handle: String,
    screenshot_url: String,
    avatar_url: String,
    tags: Array,
    selectedTag: String
  },
  computed: {
    githubUrl() {
      return `https://github.com/${this.github_handle}`;
    },
    twitterUrl() {
      return `https://twitter.com/${this.twitter_handle}`;
    }
  }
};
</script>

<style></style>
