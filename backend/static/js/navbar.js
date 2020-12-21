var vm = new Vue({
  delimiters: ["[[", "]]"],
  el: "#navbar",
  data: {
    isMenuOpen: false,
    isDropdownOpen: false,
  },
  created: function () {
    console.log(this.isMenuOpen);
    console.log(this.isDropdownOpen);
  },
});
