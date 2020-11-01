var vm = new Vue({
  delimiters: ["[[", "]]"],
  el: "#navbar",
  data: {
    isOpen: false,
  },
  created: function () {
    console.log(this.isOpen);
  },
});
