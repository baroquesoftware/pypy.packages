'use strict';

/* App Module */

// var app = angular.module('app', [
//   'ngRoute',
// ]);


// app.controller('main', function ($scope, $http) {
//     $http.get('logs/index.json').then(function(response) {
//        $scope.packages = response.data;
//     });

//     $scope.show = function(item) {
//         item[1].show = !item[1].show;
//         $http.get("logs/" + item[0] + ".txt", {
//             cache: false
//         }).then(function(response) {
//             item[1].log = response.data;
//         });
//     };
// });


$(document).ready(function() {
    var ptable = $('#ptable').DataTable( {
        "ajax": {
            "url": "logs/index.json",
            "dataSrc": ""
        },

	"columnDefs": [
            {
                "render": function ( data, type, row ) {
		    return row[1].count;
                },
                "targets": 1
            },
            {
                "render": function ( data, type, row ) {
		    if(!row[1].status){
			return '<span class="label label-success">Success</span>';
		    }
		    return '<span class="label label-danger" >Issue</span>';
                },
                "targets": 2
            },
        ]
    } );

    $('#ptable tbody').on('click', 'tr', function () {
        var data = ptable.row( this ).data();
	var fname = data[1].log;
	$.get( "logs/" + fname, function( data ) {
	    $("#log-content").html(data);
	    $('.modal').modal('show');
	});
    } );

} );
