/**
 * Created by melika on 2/22/17.
 */
(function () {
    'use strict';

    angular.module('Base', [])
        .run(function ($http, $window) {
            $http.defaults.headers.common.Authorization = 'Token ' + $window.localStorage.getItem('token');
        });
    ;
})();