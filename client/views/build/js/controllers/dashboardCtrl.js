var MainModule = angular.module("MainModule");


/////////////////////  Inverter Selection  //////////////////////
MainModule.controller("DashboardCtrl", function($scope, $http, $location, $timeout, currentUserService, currentTransactionService){
	$scope.currentUser = currentUserService.getUserDetails();
	//$scope.currentInverter = currentInverterService.getInverterDetails();
	$scope.allCompanyInverters = [];

	var self = this;

	//Seller Transaction Details
	self.sellerDetails = {
		"Ben_IFSC" : "CBIN0R10001",
		"Ben_Acct_No" : "123456789",
		"Ben_Name" : "Rohit Bhaskar",
		"Ben_Address" : "MUMBAI",
		"Ben_BankName" : "RBL",
		"Ben_BankCd" : "pureRegressionBank",
		"Ben_BranchCd" : "pureRegressionBranch",
		"Ben_Email" : "pure@regression.com",
		"Ben_Mobile" : "9969500290",
		"Ben_TrnParticulars" : "Trxn",
		"Ben_PartTrnRmks":"Success?",
		"Issue_BranchCd" : "IssueBranchCd",
		"Mode_of_Pay" : "FD",
		"Remarks" : "DMR",
		"Amount" : 2500
	}

	//Buyer Transaction Details
	self.buyerDetails = {
		"Debit_Acct_No": "123456789",
        "Debit_Acct_Name": "Tanay Shah",
        "Debit_IFSC": "RBLB1122123",
        "Debit_Mobile": "8879479102",
        "Debit_TrnParticulars": "Payment",
        "Debit_PartTrnRmks": "Remarks",
	}

/*
	$timeout(function(){
		self.buyerDetails = currentTransactionService.getBuyerDetails();
		self.sellerDetails = currentTransactionService.getSellerDetails();
	}, 500);
*/
	
	self.seeInvoice = function(){
		$location.path('/invoice');
	}

});