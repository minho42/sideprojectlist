var vm = new Vue({
  delimiters: ["[[", "]]"],
  el: "#project-list",
  data: {},
  mounted: function () {
    console.log("project_list.js");
  },
  methods: {
    upvote() {
      console.log("upvoted");
    },
  },
});
