//
// Bars chart
//

var BarsChart = (function() {

	//
	// Variables
	//

	var $chart = $('#chart-bars');


	//
	// Methods
	//

	// Init chart
	function initChart($chart) {

		// Create chart
		var ordersChart = new Chart($chart, {
			type: 'bar',
			data: {
				labels: ['class 0', 'class 1', 'class 2', 'class 3','class 4', 'class 5', 'class 6', 'class 7','class 8', 'class 9'],
				datasets: [{
					label: 'robustness',
					data: [25, 20, 30, 22, 17, 29,0,0,0,0]
				}]
			}
		});

		// Save to jQuery object
		$chart.data('chart', ordersChart);
	}


	// Init chart
	if ($chart.length) {
		initChart($chart);
	}

})();
