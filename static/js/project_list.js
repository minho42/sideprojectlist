var vm = new Vue({
  delimiters: ["[[", "]]"],
  el: "#project-list",
  data: {},
  mounted: function () {
    console.log("project_list.js");
  },
  methods: {
    upvote(project, user) {
      console.log("upvoted", project, user);
    },
  },
});
