var MainModule = angular.module("MainModule");


/////////////////////  Main Service for data sharing  //////////////////////
MainModule.service("currentDataService", function(){
	var currentData = {
		dataQuerying : true,
		labels : [],
		series : [],
		selected_modules : [],
		selected_attribute : "Efficiency",
		datasetOverride : []
	}

	var updateQueryingDetails = function(querying){
		currentData.dataQuerying = querying; 
	}
	var updateLabelDetails = function(labels){
		currentData.labels = labels;
	}
	var updateSeriesDetails = function(series){
		currentData.series = series;
	}
	var updateSelectedModules = function(selected_modules){
		currentData.selected_modules = selected_modules;
	}
	var updateSelectedAttribute = function(selected_attribute){
		currentData.selected_attribute = selected_attribute;
	}
	var updateDatasetOverride = function(datasetOverride){
		currentData.datasetOverride = datasetOverride;
	}

	var getCurrentData = function(){
		return currentData;
	}

	return{
		updateQueryingDetails : updateQueryingDetails,
		updateLabelDetails : updateLabelDetails,
		updateSeriesDetails : updateSeriesDetails,
		updateSelectedModules : updateSelectedModules,
		updateSelectedAttribute : updateSelectedAttribute,
		updateDatasetOverride : updateDatasetOverride,
		getCurrentData : getCurrentData
	}
});