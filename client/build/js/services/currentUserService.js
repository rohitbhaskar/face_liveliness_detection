var MainModule = angular.module("MainModule");


/////////////////////  Main Service for data sharing  //////////////////////
MainModule.service("currentUserService", function(){
	var currentUser = {
		// _id : "58c579edef2bf729bc032baf",
		// company_id : "1",
		// username : "rohitb1vs14",
		// contact : 1234567890,
		// email_id : "rohitb1vs14@fyp.com",
		// inverter_id : "123"
	}

	var updateUserDetails = function(user){
		currentUser = user;
	}

	var getUserDetails = function(){
		return currentUser;
	}

	return{
		updateUserDetails : updateUserDetails,
		getUserDetails : getUserDetails
	}
});
