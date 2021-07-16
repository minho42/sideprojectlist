<template>
  <div class="mx-1">
    <div class="flex items-center pt-4 pb-2 mx-4 justify-start">
      <div class="flex items-center text-2xl font-semibold">
        <div>
          <TagList
            @setSelectedTag="setSelectedTag($event)"
            :projectData="projectData"
            :selectedTag="selectedTag"
          />

          <div class="flex items-center justify-between">
            <div v-if="selectedTag">
              <div class="flex items-center justify-start ">
                <div>
                  <svg
                    class="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14"
                    ></path>
                  </svg>
                </div>

                <div>
                  {{ selectedTag }} ({{ projectDataFilteredByTag.length }})
                </div>

                <button
                  @click="selectedTag = ''"
                  class="text-green-500 hover:text-green-600 px-2 py-1"
                >
                  <svg
                    class="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    ></path>
                  </svg>
                </button>
              </div>
            </div>
            <div v-else>Projects ({{ projectData.length }})</div>

            <div v-if="!selectedTag" class="flex justify-end">
              <div
                @click="shuffle"
                class="flex items-center cursor-pointer 
              px-1 py-1 rounded-lg hover:bg-gray-300 sm:ml-2"
              >
                <div class="text-sm hidden sm:flex">
                  Shuffle
                </div>
                <button class="flex flex-col items-center">
                  <svg
                    class="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    ></path>
                  </svg>
                  <div class="text-xs flex sm:hidden">
                    Shuffle
                  </div>
                </button>
              </div>

              <div
                @click="sortAlphabetically"
                class="flex items-center cursor-pointer 
              px-1 py-1 rounded-lg hover:bg-gray-300 sm:ml-2"
              >
                <div class="text-sm hidden sm:flex">
                  A-Z
                </div>
                <button class="flex flex-col items-center">
                  <svg
                    class="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"
                    ></path>
                  </svg>
                  <div class="text-xs flex sm:hidden">
                    A-Z
                  </div>
                </button>
              </div>

              <div
                @click="sortTwitterFollowersCount"
                class="flex items-center cursor-pointer 
              px-1 py-1 rounded-lg hover:bg-gray-300 sm:ml-2"
              >
                <div class="text-sm hidden sm:flex">
                  Followers
                </div>
                <button class="flex flex-col items-center">
                  <svg
                    class="w-8 h-8"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4"
                    ></path>
                  </svg>
                  <div class="text-xs flex sm:hidden">
                    Followers
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex flex-wrap">
      <ProjectItem
        @setSelectedTag="setSelectedTag($event)"
        v-for="data in projectDataFilteredByTag"
        v-bind="data"
        :key="data.id"
        :selectedTag="selectedTag"
      />
    </div>
  </div>
</template>

<script>
import ProjectItem from "./ProjectItem.vue";
import TagList from "./TagList.vue";

export default {
  name: "ProjectList",
  data() {
    return {
      selectedTag: ""
    };
  },
  components: {
    ProjectItem,
    TagList
  },
  props: {
    projectData: Array
  },
  methods: {
    setSelectedTag(tag) {
      this.selectedTag = tag;
    },
    shuffle() {
      this.projectData.sort(() => {
        return Math.random() - 0.5;
      });
    },
    sortAlphabetically() {
      this.projectData.sort((a, b) => {
        return a.fullname > b.fullname ? 1 : a.fullname < b.fullname ? -1 : 0;
      });
    },
    sortTwitterFollowersCount() {
      this.projectData.sort((a, b) => {
        return a.twitter_followers_count < b.twitter_followers_count
          ? 1
          : a.twitter_followers_count > b.twitter_followers_count
          ? -1
          : 0;
      });
    }
  },
  computed: {
    projectDataFilteredByTag() {
      if (!this.selectedTag | (this.selectedTag === "all")) {
        return this.projectData;
      }
      return this.projectData.filter(item => {
        return item.tags.includes(this.selectedTag);
      });
    }
  },
  created() {
    this.sortTwitterFollowersCount();
  }
};
</script>
