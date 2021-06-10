//src =  'https://data.cdc.gov/resource/w9j2-ggv5.csv'
src1 = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/HI/timestamp/1542117214_A01172/TEMP.csv'
src2 = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/HI/timestamp/1552611136_A01172/TEMP.csv'
src3 = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/HI/timestamp/1554082410_A01172/TEMP.csv'
//console.log(src);

const link_prefix = 'https://raw.githubusercontent.com/jesnyder/MeasuredStress/main/';
const study_name = 'HI', format = 'timestamp', sensor = 'TEMP';
var records = ['1542117214_A01172', '1547274726_A01172', '1547276660_A01172', '1547700355_A01172', '1547782407_A01172', '1547880148_A01172'];
var src_list = [src1, src2, src3];

for(var i = 0, size = records.length; i < size ; i++){
   //var item = src_list[i];
	 src_link = link_prefix + study_name + '/' + format + '/' + records[i] + '/' + sensor + '.csv';
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
