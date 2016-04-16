$(document).ready(function(){
  var ask;
  var open;
  var low;
  var high;
  function getData() {
      var url = "http://query.yahooapis.com/v1/public/yql";
      var symbol = "{{ sym }}";
      var data = encodeURIComponent("select * from yahoo.finance.quotes where symbol in ('" + symbol + "')");

      $.getJSON(url, 'q=' + data + "&format=json&diagnostics=true&env=http://datatables.org/alltables.env")
          .done(function (data) {
            open = parseFloat(data.query.results.quote.Open);
            ask = parseFloat(data.query.results.quote.Ask);
            low = parseFloat(data.query.results.quote.DaysLow);
            high = parseFloat(data.query.results.quote.DaysHigh);
            $("#Ask").text(data.query.results.quote.Ask);
            $("#Change").text(data.query.results.quote.Change);
            $("#Open").text(data.query.results.quote.Open);
            $("#PreviousClose").text(data.query.results.quote.PreviousClose);
            $("#FiftydayMovingAverage").text(data.query.results.quote.FiftydayMovingAverage);
            $("#PercentChangeFromFiftydayMovingAverage").text(data.query.results.quote.PercentChangeFromFiftydayMovingAverage);
            $("#TwoHundreddayMovingAverage").text(data.query.results.quote.TwoHundreddayMovingAverage);
            $("#PercentChangeFromTwoHundreddayMovingAverage").text(data.query.results.quote.PercentChangeFromTwoHundreddayMovingAverage);
            $("#DaysLow").text(data.query.results.quote.DaysLow);
            $("#DaysHigh").text(data.query.results.quote.DaysHigh);
            $("#YearLow").text(data.query.results.quote.YearLow);
            $("#YearHigh").text(data.query.results.quote.YearHigh);
            $("#EarningsShare").text(data.query.results.quote.EarningsShare);
            $("#EPSEstimateNextQuarter").text(data.query.results.quote.EPSEstimateNextQuarter);
            $("#EPSEstimateCurrentYear").text(data.query.results.quote.EPSEstimateCurrentYear);
            $("#EPSEstimateNextYear").text(data.query.results.quote.EPSEstimateNextYear);

          })
          .fail(function (jqxhr, textStatus, error) {
          var err = textStatus + ", " + error;
              $("#result").text('Request failed: ' + err);
      });
  }
  getData();

  window.onload = function () {
    var data_list = {{ canvas_list|safe }};
    var candle_points = [];
    for (x = 0; x < data_list.length; x++) {
      candle_points.push({ x: new Date(data_list[x][0], data_list[x][1], data_list[x][2]),
                           y: [ data_list[x][3], data_list[x][4], data_list[x][5], data_list[x][6] ],
                           color: "Black",
                           borderColor: "#BF0000"});
    }

  	var chart = new CanvasJS.Chart("chartContainer",
  	{
  		title:{
  			text: "CanvasJS Candlestick Chart",
  		},
  		exportEnabled: true,
  		axisY: {
  			includeZero: false,
  			prefix: "$",
        stripLines:[
              {
                  value:112.04,
                  color:"#BF0000",
                  label : "112.04",
                  labelFontColor: "#BF0000",
                  lineDashType: "dash"
              }
              ]
  		},
  		axisX: {
  			valueFormatString: "DD-MMM",
  		},
  		data: [
  		{
  			type: "candlestick",
  			dataPoints: candle_points
  		}
  		]
  	});
  	chart.render();

    var updateChart = function () {

      getData();
      console.log(ask);
      chart.options.data[0].dataPoints[chart.options.data[0].dataPoints.length-1].y = [open, high, low, ask];
      // chart.options.data[0].dataPoints.shift();
      chart.options.axisY.stripLines[0].value = ask;
      chart.options.axisY.stripLines[0].label = ask;
      // dataPoints.push({
      //   y : parseFloat(ask)
      // });


      // chart.options.title.text = "Update " + updateCount;
      chart.render();

     };

  // update chart every second
  setInterval(function(){updateChart()}, 1500);

  }
});