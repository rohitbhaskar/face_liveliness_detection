var MainModule = angular.module("MainModule");


/////////////////////  MainModule Page Controller  //////////////////////
MainModule.controller("UsersCtrl", function($scope, $http, currentUserService){
	$scope.currentUser = currentUserService.getUserDetails();
	$scope.allCompanyUsers = [];

	$http({
      method: 'GET',
      url: 'http://localhost:3000/users',
      params: {company_id: $scope.currentUser.company_id}
    }).then(function successCallback(response) {
      console.log(response);
      $scope.allCompanyUsers = response.data;
    }, function errorCallback(response) {
      console.log(response);
    });
});