'use strict';

/* App Module */

var app = angular.module('app', [
  'ngRoute',
]);


app.controller('main', function ($scope, $http) {
    $http.get('logs/index.json').then(function(response) {
        $scope.packages = response.data;
    });

    $scope.show = function(item) {
        item[1].show = !item[1].show;

        $http.get("logs/" + item[0] + ".txt").then(function(response) {
            item[1].log = response.data;
        });
    };
    // $scope.phones = [
    //     {'name': 'Nexus S',
    //      'snippet': 'Fast just got faster with Nexus S.'},
    //     {'name': 'Motorola XOOM™ with Wi-Fi',
    //      'snippet': 'The Next, Next Generation tablet.'},
    //     {'name': 'MOTOROLA XOOM™',
    //      'snippet': 'The Next, Next Generation tablet.'}
    // ];
});

// app.config(['$routeProvider',
//   function($routeProvider) {
//       $routeProvider.when('/phones', {
//         templateUrl: 'partials/phone-list.html',
//         controller: 'PhoneListCtrl'
//       });

//       // when('/phones/:phoneId', {
//       //   templateUrl: 'partials/phone-detail.html',
//       //   controller: 'PhoneDetailCtrl'
//       // }).
//       // otherwise({
//       //   redirectTo: '/phones'
//       // });
//   }]);
