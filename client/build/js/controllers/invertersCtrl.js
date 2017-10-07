var MainModule = angular.module("MainModule");


/////////////////////  Inverter Selection  //////////////////////
MainModule.controller("InverterCtrl", function($scope, $http, $location, currentUserService, currentInverterService, inverterDataService){
	$scope.currentUser = currentUserService.getUserDetails();
	$scope.currentInverter = currentInverterService.getInverterDetails();
	$scope.allCompanyInverters = [];

	setTimeout(function(){
		$('#datatable-responsive').DataTable();   
	}, 0);

	$http({
      method: 'GET',
      url: 'http://localhost:3000/inverters',
      params: {company_id: $scope.currentInverter.company_id}
    }).then(function successCallback(response) {
      console.log(response);
      $scope.allCompanyInverters = response.data;
    }, function errorCallback(response) {
      console.log(response);
    });
	

	$scope.newInverter = {};

	$scope.addNewInverter = function(inverter){
		$http({
	      method: 'POST',
	      url: 'http://localhost:3000/inverters',
	      data: inverter
	    }).then(function successCallback(response) {
	      console.log(response);
	    }, function errorCallback(response) {
	      console.log(response);
	    });
	}


	// Choosing an inverter from the list //
	var selectedInverter = {};
	$scope.selectCheckbox = function(index){
		selectedInverter = $scope.allCompanyInverters[index];
		for(i=0; i<$scope.allCompanyInverters.length; i++){
			if(i != index){
				$scope.allCompanyInverters[i].checked == false;
			}
		}
	}
	$scope.selectInverter = function(){
		if(!angular.equals(selectedInverter, {})){
			for(i=0; i<$scope.allCompanyInverters.length; i++)
				$scope.allCompanyInverters[i].checked == false;

			var date = new Date();
			var today = date.getFullYear() + "-" + date.getMonth() + "-" + date.getDate()
			inverterDataService.queryInverterData('2017-01-24', '2017-01-24');
			$location.path('/dashboard');
			currentInverterService.updateInverterDetails(selectedInverter);
		}
	}
});