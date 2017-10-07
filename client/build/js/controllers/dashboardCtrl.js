var MainModule = angular.module("MainModule");


/////////////////////////////  Main Page Controller  ////////////////////////////
MainModule.controller("DashboardCtrl", function($scope, $http, currentUserService, currentInverterService, inverterDataService, currentDataService){
  //$rootScope.$emit('received-inverter-data');
  var currentUser = currentUserService.getUserDetails();
  var currentInverter = currentInverterService.getInverterDetails();
  var currentData = currentDataService.getCurrentData();

  var newDate = new Date();
  var todaysDate = (newDate.getMonth()+1) + '/' + newDate.getDate() + '/' + newDate.getFullYear().toString().slice(-2);

  ////////////// Main Graph Setup //////////////
  var datasetOverride_refrence = [{
    backgroundColor: "rgba(157, 190, 207, 0.15)",
    borderColor: "rgba(157, 190, 207, 1)",
    pointBorderColor: "rgba(157, 190, 207, 0.7)",
    pointBackgroundColor: "rgba(157, 190, 207, 0.7)",
    pointHoverBackgroundColor: "rgba(157, 190, 207, 1)",
    pointHoverBorderColor: "rgba(220,220,220,1)"
  }, {
    backgroundColor: "rgba(181, 181, 181, 0.15)",
    borderColor: "rgba(181, 181, 181, 1)",
    pointBorderColor: "rgba(181, 181, 181, 0.7)",
    pointBackgroundColor: "rgba(181, 181, 181, 0.7)",
    pointHoverBackgroundColor: "rgba(181, 181, 181, 1)",
    pointHoverBorderColor: "rgba(220,220,220,1)"
  }, {
    backgroundColor: "rgba(247, 70, 74, 0.15)",
    borderColor: "rgba(247, 70, 74, 1)",
    pointBorderColor: "rgba(247, 70, 74, 0.7)",
    pointBackgroundColor: "rgba(247, 70, 74, 0.7)",
    pointHoverBackgroundColor: "rgba(247, 70, 74, 1)",
    pointHoverBorderColor: "rgba(220,220,220,1)"
  }, {
    backgroundColor: "rgba(70, 191, 189, 0.15)",
    borderColor: "rgba(70, 191, 189, 1)",
    pointBorderColor: "rgba(70, 191, 189, 0.7)",
    pointBackgroundColor: "rgba(70, 191, 189, 0.7)",
    pointHoverBackgroundColor: "rgba(70, 191, 189, 1)",
    pointHoverBorderColor: "rgba(220,220,220,1)"
  }];
  var series_refrence = ['inverter', 'module1', 'module2', 'module3'];

  $scope.labels = currentData.labels;//"January", "February", "March", "April", "May", "June", "July"
  $scope.series = currentData.series;
  $scope.data  = [];
  $scope.datasetOverride = currentData.datasetOverride;
  $scope.options = {
  };
    $scope.onClick = function (points, evt) {
    console.log(points, evt);
  };
  // End of Main Graph Setup //


  ////////////////// hide options till data loads & load 1st data ////////////////////
  $scope.dataQuerying = currentData.dataQuerying;
  //$scope.labels = inverterDataService.getInverterData(1, 'Time');
  inverterDataService.checkInverterData($scope, function dataReceived(){
    $scope.dataQuerying = false;
    currentDataService.updateQueryingDetails($scope.dataQuerying);

    $scope.labels = inverterDataService.getInverterData(1, 'timestamp');
    currentDataService.updateLabelDetails($scope.labels);

    $scope.toggle($scope.all_modules[1].value);
    currentDataService.updateSelectedModules($scope.all_modules[1].value);

    $scope.chooseAttribute($scope.graph_details.selected_attribute);
  });


  // All Graph Attributes //
  $scope.graph_details = {
    selected_attribute : currentData.selected_attribute,
    selected_modules : currentData.selected_modules
  }

  ///////////// CheckBox Functionality //////////////
  $scope.addToGraph = function(id){
    $scope.data.push(inverterDataService.getInverterData(id, $scope.graph_details.selected_attribute));
    $scope.series.push(series_refrence[id]);
    currentDataService.updateSeriesDetails($scope.series);
    $scope.datasetOverride.push(datasetOverride_refrence[id]);
    currentDataService.updateDatasetOverride($scope.datasetOverride);
  };
  $scope.removeFromGraph = function(id){
    $scope.data.splice(id, 1);
    $scope.series.splice(id, 1);
    currentDataService.updateSeriesDetails($scope.series);
    $scope.datasetOverride.splice(id, 1);
    currentDataService.updateDatasetOverride($scope.datasetOverride);
  } ;
  // Check boxes to choose modules //
  $scope.all_modules = [{
    name: 'Inverter',
    value: 'inverter'
  },{
    name: 'Module 1',
    value: 'module1'
  },{
    name: 'Module 2',
    value: 'module2'
  },{
    name: 'Module 3',
    value: 'module3'
  }];
  $scope.toggle = function (item) {
    var idx = $scope.graph_details.selected_modules.indexOf(item);
    if (idx > -1) {
      $scope.graph_details.selected_modules.splice(idx, 1);
      currentDataService.updateSelectedModules($scope.graph_details.selected_modules);
      $scope.removeFromGraph(idx);
    }
    else {
      $scope.graph_details.selected_modules.push(item);
      currentDataService.updateSelectedModules($scope.graph_details.selected_modules);
      var id = series_refrence.indexOf(item);
      $scope.addToGraph(id);
    }
    $scope.radioBtnDisable();
  };
  $scope.exists = function (item) {
    return $scope.graph_details.selected_modules.indexOf(item) > -1;
  };


  //////////////// Radio Buttons Functionality ////////////////
  $scope.all_attributes = [{
    name: 'DC Voltage',
    value: 'Vdc',
    btn_disable: false
  },{
    name: 'DC Current',
    value: 'Idc',
    btn_disable: false
  },{
    name: 'DC Power',
    value: 'Pow_dc',
    btn_disable: false
  },{
    name: 'Grid Voltage',
    value: 'GridVolt',
    btn_disable: false
  },{
    name: 'Grid Current',
    value: 'GridCurr',
    btn_disable: false
  },{
    name: 'Grid Power',
    value: 'GridP',
    btn_disable: false
  },{
    name: 'Efficiency',
    value: 'Efficiency',
    btn_disable: false
  }];
  $scope.chooseAttribute = function(attribute){
    currentDataService.updateSelectedAttribute(attribute);
    for(i=0; i<$scope.graph_details.selected_modules.length; i++){
      if($scope.graph_details.selected_modules[i] == 'module1')
        $scope.data[i] = inverterDataService.getInverterData(1, attribute);
      else if($scope.graph_details.selected_modules[i] == 'module2')
        $scope.data[i] = inverterDataService.getInverterData(2, attribute);
      else if($scope.graph_details.selected_modules[i] == 'module3')
        $scope.data[i] = inverterDataService.getInverterData(3, attribute);
      else
        $scope.data[i] = inverterDataService.getInverterData(0, attribute);
    }
  }
  $scope.chooseAttribute($scope.graph_details.selected_attribute);
  $scope.radioBtnDisable = function(){
    var ids = [0, 1, 2, 6];
    var inv_id = $scope.exists('inverter');
    if(inv_id){
      for(i=0; i<ids.length; i++)
        $scope.all_attributes[ids[i]].btn_disable = true;
    }
    else{
      for(i=0; i<$scope.all_attributes.length; i++)
        $scope.all_attributes[i].btn_disable = false;
    }
  }


  // Eventlog //
  $scope.getModuleData = function(){
    // Events Request //
    $scope.allEvents = [];
    for(i=0; i<3; i++){
      $http({
        method: 'GET',
        url: 'http://localhost:3000/events',
        params: {inverter_id: currentInverter._id , Category: i + 1, Date: '1/24/17'}
      }).then(function successCallback(response) {
        if(response.data[0].Category == '1')
          $scope.allEvents[0] = response.data;
        else if(response.data[0].Category == '2')
          $scope.allEvents[1] = response.data;
        else
          $scope.allEvents[2] = response.data;
      }, function errorCallback(response) {
        console.log(response);
      });
    }
  }


  // Date Selector //
  $scope.startDate="";
  $scope.endDate="";
  $(document).ready(function() {

    var cb = function(start, end, label) {
      console.log(start.toISOString(), end.toISOString(), label);
      $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
      $scope.startDate = start.format('YYYY-MM-DD');
      $scope.endDate = end.format('YYYY-MM-DD');

      console.log("startDate ", $scope.startDate);
      console.log("endDate ", $scope.endDate);
      $scope.$apply();
      inverterDataService.queryInverterData($scope.startDate, $scope.endDate);
    };
    var optionSet1 = {
      startDate: moment().subtract(29, 'days'),
      endDate: moment(),
      minDate: '01/01/2012',
      maxDate: todaysDate,
      dateLimit: {
        days: 365
      },
      showDropdowns: true,
      showWeekNumbers: true,
      timePicker: false,
      timePickerIncrement: 1,
      timePicker12Hour: true,
      ranges: {
        'Today': [moment(), moment()],
        'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days': [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month': [moment().startOf('month'), moment().endOf('month')],
        'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      },
      opens: 'left',
      buttonClasses: ['btn btn-default'],
      applyClass: 'btn-small btn-primary',
      cancelClass: 'btn-small',
      format: 'MM/DD/YYYY',
      separator: ' to ',
      locale: {
        applyLabel: 'Submit',
        cancelLabel: 'Clear',
        fromLabel: 'From',
        toLabel: 'To',
        customRangeLabel: 'Custom',
        daysOfWeek: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
        monthNames: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        firstDay: 1
      }
    };
    $('#reportrange span').html(moment().subtract(29, 'days').format('MMMM D, YYYY') + ' - ' + moment().format('MMMM D, YYYY'));
    $('#reportrange').daterangepicker(optionSet1, cb);
    $('#options1').click(function() {
      $('#reportrange').data('daterangepicker').setOptions(optionSet1, cb);
    });
    $('#options2').click(function() {
      $('#reportrange').data('daterangepicker').setOptions(optionSet2, cb);
    });
    $('#destroy').click(function() {
      $('#reportrange').data('daterangepicker').remove();
    });
  });



});
