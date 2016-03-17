'use strict';

/* App Module */

var app = angular.module('app', [
  'ngRoute', 'ngSanitize'
]);


app.controller('main', function ($scope, $http, $location, $timeout, $anchorScroll) {
    $http.get('logs/index.json').then(function(response) {
        $scope.packages = response.data;
        $timeout(function() {
            $anchorScroll();
        });
    });

    $scope.notes = notes;

    $scope.show = function(item) {
        item[1].show = !item[1].show;
        $http.get("logs/" + item[0] + ".txt", {
            cache: false
        }).then(function(response) {
            item[1].log = response.data;
            $location.hash(item[0]);
        });
    };
});

