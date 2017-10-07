var MainModule = angular.module("MainModule");


/////////////////////  Main Service for data sharing  //////////////////////
MainModule.service("inverterDataService", function($http, currentInverterService, $rootScope){
    // Global variables for sharing data //
	var inverterData = {
	}
	var moduleData = [{}, {}, {}];

	// Get Todays Data //
	var date = new Date();
	var today = date.getMonth() + '/' + date.getDate() + '/' + date.getFullYear().toString().slice(2, 2);
	
	var queryForData = function(startDate, endDate){
		var currentInverter = currentInverterService.getInverterDetails();

		for(i=1; i<4; i++){
			$http({
		      method: 'GET',
		      url: 'http://localhost:3000/module_data',
		      params: {
		      	query:{
			      	timestamp: {$gte: startDate, $lte: endDate},
			      	inverter_id: currentInverter._id,
			      	module: i
			      },
		      	fields:{module:1, Vdc:1, Idc:1, Pow_dc:1, GridVolt:1, GridCurr:1, GridP:1, Efficiency:1, timestamp:1},
		      	key:["module", "Vdc", "Idc", "Pow_dc", "GridVolt", "GridCurr", "GridP", "Efficiency", "timestamp"]
		      }
		    }).then(function successCallback(response) {
		      console.log(response);
		      if(response.data.module[0] == 1)
		      	moduleData[0] = response.data;
		      else if(response.data.module[0] == 2)
		      	moduleData[1] = response.data;
		      else{
		      	moduleData[2] = response.data;
		      	$rootScope.$emit('received-inverter-data');
		      }
		    }, function errorCallback(response) {
		      console.log(response);
		    });
		}
		$http({
	      method: 'GET',
	      url: 'http://localhost:3000/inverter_data',
	      params: {
	      	query:{
		      	timestamp: {$gte: startDate, $lte: endDate},
		      	inverter_id:currentInverter._id,
		      	//module:i
		      },
	      	fields:{GridVolt:1, GridCurr:1, GridP:1},
	      	key:["GridVolt", "GridCurr", "GridP"]
	      }
	    }).then(function successCallback(response) {
	      console.log('inverter_data is:', response);
	      inverterData = response.data;
	    }, function errorCallback(response) {
	      console.log(response);
	    });
	}
	//queryForData('1/24/17');



	// Service Methods //
	var queryInverterData = function(startDate, endDate){
		// Convert to ISO Date Strings //
		if(startDate == endDate){
			startDate = startDate + 'T00:00:00.000Z'
			endDate = endDate + 'T23:59:59.000Z'
		}
		else{
			startDate = startDate + 'T00:00:00.000Z';
			endDate = endDate + 'T00:00:00.000Z';
		}
		queryForData(startDate, endDate);
	}

	var checkInverterData = function(scope, callback){
		var handler = $rootScope.$on('received-inverter-data', callback);
		scope.$on('$destroy', handler);
	}

	var updateInverterData = function(inverter_data){
		inverterData = inverter_data;
	}

	var getInverterData = function(id, attribute){
		if(id == 0){
			return inverterData[attribute]
		}
		else
			return moduleData[id-1][attribute]//.slice(3124, 3131);
	}

	return{
		queryInverterData : queryInverterData,
		checkInverterData : checkInverterData,
		updateInverterData : updateInverterData,
		getInverterData : getInverterData
	}
});



