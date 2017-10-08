(function(){

/////////////////////  Main Module  //////////////////////
var MainModule = angular.module("MainModule", ['ngRoute']);


MainModule.config(function($routeProvider) {
  /*$mdThemingProvider.theme('default')
    .primaryPalette('blue-grey')
    .accentPalette('teal'); */

// Main Routing //
  $routeProvider
	    .when("/", {
	        templateUrl : "transactions.html",
	        controller: "TransactionCtrl",
	        controllerAs: "tc"
	    })
	    .when("/transactions", {
	        templateUrl : "transactions.html",
	        controller: "TransactionCtrl",
	        controllerAs: "tc"
	    })
	    .when("/users", {
	        templateUrl : "users.html",
	        controller: "UsersCtrl"
	    })
	    .when("/dashboard", {
	        templateUrl : "dashboard.html",
	        controller: "InverterCtrl",
          controllerAs: "dashboard"
	    })
	    .when("/addInverter", {
	        templateUrl : "add_inverter.html",
	        controller: "InverterCtrl"
	    })
      .when("/prediction", {
          templateUrl : "predicted_data.html",
          controller: "InverterCtrl"
      })
});



/////////////////////  Main Page Controller  //////////////////////
MainModule.controller("MainCtrl", function($scope, $http, currentUserService){
  
  // Update Current Users Sercice //
  $scope.currentUser = localStorage.getItem("full_user");
  //localStorage.clear();
  $scope.currentUser = JSON.parse($scope.currentUser);
  delete $scope.currentUser.password;
  currentUserService.updateUserDetails($scope.currentUser)
});




/////////////////////  Add New Inverter  //////////////////////
MainModule.controller("NewInverterCtrl",["$scope", function($scope){
	
}]);


})();