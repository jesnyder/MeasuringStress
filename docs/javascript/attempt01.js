// https://raw.githubusercontent.com/jesnyder/MeasuringStress/master/studies/HI/formatted/clean/1547700355_A01172/All/EDA.csv?token=ADBFXFHQMXOIXRWQNYCYQ7DAXKTE6
const link_prefix = 'https://raw.githubusercontent.com/jesnyder/MeasuringStress/master/studies/';
cont link_token = '?token=ADBFXFHQMXOIXRWQNYCYQ7DAXKTE6'
var sensor_list = ['ACC', 'BVP', 'EDA', 'HR', 'TEMP'];
var study_list = ['HI', 'PMR'];
var format_list = ['source', 'truncate', 'coregister', 'clean', 'regression', 'statistics' ];

const study = 'HI', format = 'clean', segment = 'All', sensor = 'EDA';
var records = ['1554748372_A01609', '1554748372_A01609'];

for(var i = 0, size = records.length; i < size ; i++){
	 src_link = link_prefix + study + '/' + 'formatted' + '/' + format + '/' + records[i] + '/' + segment + '/' + sensor + '.csv' + link_token;
	 src_link = 'https://raw.githubusercontent.com/jesnyder/MeasuringStress/master/studies/HI/formatted/clean/1554748372_A01609/All/EDA.csv'
	 plot(src_link, i);
}


function plot(src, i) {
	fetch(src)
		.then(function (response) {
			return response.text();
		})
		.then(function (text) {
			let series = csvToSeries(text);
			renderChart(series, i);
		})
		.catch(function (error) {
			//Something went wrong
			console.log(error);
		});
	}


function csvToSeries(text) {
	const time = 'timeMinutes';
	// const meas = 'measurement';
	const meas = 'A01172_measurement';
	let dataAsJson = JSC.csv2Json(text);
	let source = [];
	dataAsJson.forEach(function (row) {
		source.push({x: row[time], y: row[meas]});
		//add either to male, female, or discard.

	});
	return [
		{name: 'Source', points: source},
		//{name: 'Source', points: source}
	];
}

function renderChart(series, i){
	const chartDiv = 'chartDiv' + i
	JSC.Chart(chartDiv, {
		title_label_text: 'Record: ' + i,
		annotations: [{
			label_text: 'Source: Empatica E4 Wearables',
			position: 'bottom left'
		}],
        legend_visible: false,
		defaultSeries_lastPoint_label_text: '<b>%seriesName</b>',
		//defaultPoint_tooltip: '%seriesName <b>%yValue</b> degrees',
		defaultPoint_tooltip: '<b>%yValue</b> degrees',
		xAxis_crosshair_enabled: true,
		series: series
	});


}
