var MainModule = angular.module("MainModule");


/////////////////////  Main Service for data sharing  //////////////////////
MainModule.service("currentInverterService", function(){
	var currentInverter = {
		// "_id" : "58d2a7f42ae554bb8a9024bd",
		// "company_id" : "1",
		// "serial_no" : "123",
		// "comm_date" : "2017/02/01",
		// "firmware_version" : "1.0.0",
		// "firware_update" : "2017/02/20",
		// "location" : "Haridwar",
		// "ip" : "127.0.0.1",
		// "username" : "rohit",
		// "password" : "abcd1234",
		// "inverter_id" : "58d2a7f42ae554bb8a9024bd"
	}

	var updateInverterDetails = function(Inverter){
		currentInverter = Inverter;
	}

	var getInverterDetails = function(){
		return currentInverter;
	}

	return{
		updateInverterDetails : updateInverterDetails,
		getInverterDetails : getInverterDetails
	}
});
