var MainModule = angular.module("MainModule");


/////////////////////  Main Page Controller  //////////////////////
MainModule.controller("PredictCtrl", function($scope, $http, currentInverterService){
  $scope.currentInverter = {};
  //$scope.currentUser = currentUserService.getUserDetails();
  $scope.currentInverter = currentInverterService.getInverterDetails();
  $scope.predictedData = {};
  

  $scope.getPredictedData = function(){
    $http({
      method: 'GET',
      url: 'http://localhost:3000/predict',
      params: {query:{name : "module1", inverter_id:$scope.currentInverter._id}, fields:{timestamp:1, GridCurr:1, Vdc:1, Idc:1}, key:["Time", "GridCurrent", "Input DC Voltage", "Input DC Current"]}
    }).then(function successCallback(response) {
      console.log(response);
      $scope.predictedData.yAxis = response.data.GridCurr;
      $scope.predictedData.xAxis = response.data.timestamp;

      // Plotting the dashboard graph //
      var ftx = document.getElementById("forecast_chart");
      var forecast_chart = new Chart(ftx, {
        type: 'line',
        data: {
          labels: $scope.predictedData.xAxis,
          datasets: [{
            label: "Module 1 Predicted Data",
            backgroundColor: "rgba(38, 185, 154, 0.31)",
            borderColor: "rgba(38, 185, 154, 0.7)",
            pointBorderColor: "rgba(38, 185, 154, 0.7)",
            pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointBorderWidth: 1,
            data: $scope.predictedData.yAxis
            }/*, {
            label: "Module 2",
            backgroundColor: "rgba(3, 88, 106, 0.3)",
            borderColor: "rgba(3, 88, 106, 0.70)",
            pointBorderColor: "rgba(3, 88, 106, 0.70)",
            pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(151,187,205,1)",
            pointBorderWidth: 1,
            data: [82, 23, 66, 9, 99, 4, 2]
            }*/]
        }
      });
    }, function errorCallback(response) {
      console.log(response);
    });
 }

});