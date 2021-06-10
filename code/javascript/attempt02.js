//src =  'https://data.cdc.gov/resource/w9j2-ggv5.csv'
src3 = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/HI/timestamp/1542117214_A01172/TEMP.csv'
src = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/HI/timestamp/1552611136_A01172/TEMP.csv'
src2 = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/HI/timestamp/1554082410_A01172/TEMP.csv'
//console.log(src);

var src_list = [src, src2, src3];

for(var i = 0, size = src_list.length; i < size ; i++){
   var item = src_list[i];
	 plot(item)
}


function plot(src) {
	fetch(src)
		.then(function (response) {
			return response.text();
		})
		.then(function (text) {
			let series = csvToSeries(text);
			renderChart(series);
		})
		.catch(function (error) {
			//Something went wrong
			console.log(error);
		});
	}


function csvToSeries(text) {
	const lifeExp = 'average_life_expectancy';
	const time = 'timeMinutes';
	const meas = 'measurement';
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

function renderChart(series){
	JSC.Chart('chartDiv2', {
		title_label_text: 'Record: ' + src,
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
