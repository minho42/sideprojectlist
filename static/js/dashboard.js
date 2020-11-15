const SIGNUP_STEPSIZE = 5;

Vue.component("signupcount-linechart", {
  props: ["name", "labels", "series"],
  template: '<canvas id="signupcount-linechart"></canvas>',

  data() {
    return {
      myChart: undefined,
    };
  },
  methods: {
    getMax() {
      var max = Math.max.apply(null, this.series[0]) + 1;
      var roundedMax = Math.ceil(max / SIGNUP_STEPSIZE) * SIGNUP_STEPSIZE;
      return roundedMax;
    },
    fetchData() {
      console.log("fetchData()");
      this.myChart.config.options.scales.yAxes[0].ticks.max = this.getMax();
      this.myChart.config.options.scales.yAxes[0].ticks.stepSize = SIGNUP_STEPSIZE;

      this.myChart.config.data.labels = this.labels;
      this.myChart.config.data.datasets[0].data = this.series[0];

      this.myChart.update();
    },
  },
  watch: {
    labels: "fetchData",
    series: "fetchData",
  },
  // https://www.chartjs.org/docs/latest/configuration/elements.html
  mounted: function () {
    console.log("mounted function");
    var data = {
      // https://www.chartjs.org/docs/latest/charts/line.html#dataset-properties
      datasets: [
        {
          fill: false,
          borderColor: "#48b884",
          pointRadius: "",
          // steppedLine: "before",
        },
      ],
    };

    var options = {
      title: {
        display: true,
        text: "Signups",
        fontSize: 16,
        fontColor: "#212529",
        fontStyle: "",
      },
      responsive: true,
      maintainAspectRatio: false,
      showLines: true,
      snapGaps: true,

      legend: {
        display: false,
      },
      scales: {
        yAxes: [
          {
            gridLines: {
              display: true,
            },
            ticks: {
              display: true,
              min: 0,
              max: 0,
              stepSize: 1,
            },
          },
        ],
        xAxes: [
          {
            gridLines: {
              display: false,
            },
            // https://www.chartjs.org/docs/latest/axes/cartesian/#tick-configuration
            ticks: {
              maxRotation: 0,
              display: false,
            },
          },
        ],
      },
      // https://www.chartjs.org/docs/latest/configuration/tooltip.html
      tooltips: {
        enabled: false,
      },
    };
    var ctx = document.getElementById("signupcount-linechart").getContext("2d");
    this.myChart = new Chart(ctx, {
      type: "line",
      data: data,
      options: options,
    });
  },
});

var vm = new Vue({
  delimiters: ["[[", "]]"],
  el: "#dashboard",
  data: {
    signupCountName: "signupcount",
    signupDateLabels: [],
    signupCountSeries: [],
  },
  mounted: function () {
    this.getSignupCount();
  },
  methods: {
    saveInfoForAll() {
      console.log("saveInfoForAll");
      axios
        .get("/api/save-info-for-all/")
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log("saveInfoForAll().axios.get error: " + error.message);
        });
    },
    getSignupCount() {
      console.log("getSignupCount()");
      var self = this;
      axios
        .get("/api/signup-count/")
        .then(function (response) {
          console.log(response.data);
          self.signupDateLabels = response.data.dates;
          self.signupCountSeries = [response.data.counts];
        })
        .catch(function (error) {
          console.log("getSignupCount().axios.get error: " + error.message);
        });
    },
  },
});
