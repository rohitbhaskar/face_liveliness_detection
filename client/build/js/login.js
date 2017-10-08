(function(){

////////////////////  Login Module and Controller  //////////////////////
var LoginModule = angular.module("LoginModule", ['ngRoute']);


// Ng-View Routing //
LoginModule.config(function($routeProvider) {
// Login Routing //
  $routeProvider
      .when("/", {
          templateUrl : "/html/login/login_form.html",
          controller: "LoginCtrl"
      })
      .when("/signin", {
          templateUrl : "/html/login/login_form.html",
          controller: "LoginCtrl"
      })
      .when("/signup", {
          templateUrl : "/html/login/register_form.html",
          controller: "RegisterCtrl"
      })
});



// Login Controller for authentication //
LoginModule.controller('LoginCtrl', function($scope, $http){
	$scope.login_username = "";
	$scope.login_password = "";
  $scope.data = new Array();

  var user = {};
  $scope.authenticateUser = function(){
    for(var i=0; i<login_credentials.length; i++){
      var username = $scope.login_username;
      var password = $scope.login_password;
      user[username] = password;
      if(JSON.stringify(login_credentials[i]) == JSON.stringify(user)){
        loggedIn();
      }
    }
    //$scope.error_mssg = "Wrong username or password";
  };

  loggedIn = function(){
    localStorage.clear();
    localStorage.setItem("full_user", JSON.stringify(user));

    // redirect to main page //
    window.location.href='/html/main.html';
  }

  var login_credentials = [{"rohit": "abcd1234"}, {"user1234":"abcd1234"}, {"tanay":"abcd1234"}];
});


// New User Registration //
LoginModule.controller('RegisterCtrl', function($scope, $http){
  $scope.registerError = "";
  $scope.newUser = {
    "username" : "",
    "password" : "",
    "company_id" : null,
    "contact" : null,
    "email_id" : "",
    "inverter_id" : ""
  }

  $scope.addNewUser = function(){
    $http({
      method: 'POST',
      url: 'http://localhost:3000/users',
      data: $scope.newUser
    }).then(function successCallback(response) {
      console.log(response);
      if(response.data.ok == 1){
        localStorage.setItem("full_user", JSON.stringify($scope.newUser));
        // redirect to main page //
        window.location.href='/html/main.html';
      }
      else{
        $scope.registerError = "Some error occured";
      }
    }, function errorCallback(response) {
      console.log(response);
    });
  }
});

})();