var MainModule = angular.module("MainModule");

MainModule.controller("TransactionCtrl", function($scope, $http, $location, $timeout, currentTransactionService){
	var self = this;
	
	$scope.transaction_id = 0;

	var sellerTxId = 0;
	var buyerTxId = 0;

	var sellerAadhaar = 688160177038;
	var buyerAadhaar = 868686194455;

	var OTPRequest = {
		"GenerateOTP": { 
			"Header": {
				"TranID": "", 
				"Corp_ID": "HACKTEST"
			}, 
			"Body": {
				"aadharNo": ""
			},
			"Signature": {
				"Signature": ""
			}
		}
	}

	//Seller Transaction Details
	self.sellerDetails = {
		"Ben_IFSC" : "CBIN0R10001",
		"Ben_Acct_No" : "",
		"Ben_Name" : "",
		"Ben_Address" : "MUMBAI",
		"Ben_BankName" : "RBL",
		"Ben_BankCd" : "pureRegressionBank",
		"Ben_BranchCd" : "pureRegressionBranch",
		"Ben_Email" : "pure@regression.com",
		"Ben_Mobile" : "",
		"Ben_TrnParticulars" : "Trxn",
		"Ben_PartTrnRmks":"Success?",
		"Issue_BranchCd" : "IssueBranchCd",
		"Mode_of_Pay" : "FD",
		"Remarks" : "DMR",
		"Amount" : 1
	}

	//Buyer Transaction Details
	self.buyerDetails = {
		"Debit_Acct_No": "",
        "Debit_Acct_Name": "",
        "Debit_IFSC": "RBLB1122123",
        "Debit_Mobile": "",
        "Debit_TrnParticulars": "Payment",
        "Debit_PartTrnRmks": "Remarks",
	}


	self.sellerDetailsResetClick = function(){
		self.sellerDetails.Ben_Acct_No = "";
		self.sellerDetails.Ben_Name = "";
		self.sellerDetails.Ben_Mobile = "";
	}

	self.getOTP = function(id){
		//var localSellerDetails = {};

		//Seller -> 1
		if(id == 1){
			//angular.copy(self.sellerDetails, localSellerDetails);
			
			//New Tx Id
			sellerTxId = Math.floor((Math.random()*8000000) + 1000000);
			
			//Edit the OTP Request object
			OTPRequest.GenerateOTP.Body.aadharNo = sellerAadhaar.toString();
			OTPRequest.GenerateOTP.Header.TranID = sellerTxId.toString();
		}

		//Buyer -> 0
		else{
			buyerTxId = Math.floor((Math.random()*8000000) + 1000000);

			//Edit the OTP Request object
			OTPRequest.GenerateOTP.Body.aadharNo = buyerAadhaar.toString();
			OTPRequest.GenerateOTP.Header.TranID = buyerTxId.toString();
		}

		//Http Request
		$http({
			  method: 'POST',
			  url: 'https://api.us.apiconnect.ibmcloud.com/rbl/rblhackathon/rbl/v1/Esigngeneration/generateotp?client_id=b6638488-c531-4ae9-b2be-6656d1ac7bff&client_secret=J2aO7pJ2xN4tQ8iW3kO1pE2nU7hA0dU5gL1iN4dV1xK1mT3mG4',
			  headers: {"Content-Type":"application/json"},
			  data: OTPRequest
			}).then(function successCallback(response) {
			    // this callback will be called asynchronously
			    // when the response is available
			    console.log("success otp generation: ", response);
			  }, function errorCallback(response) {
			  	console.log("error otp generation: ", response);
			    // called asynchronously if an error occurs
			    // or server returns response with an error status.
			  });
		
	}


	self.completeTransaction = function(){
		currentTransactionService.updateTxDetails(self.buyerDetails, self.sellerDetails);
		$timeout(function(){$location.path('/dashboard');}, 1000);
	}
	
});