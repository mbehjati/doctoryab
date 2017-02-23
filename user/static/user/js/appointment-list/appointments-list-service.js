/**
 * Created by melika on 2/23/17.
 */

(function () {
    'use strict';
    angular
        .module('Base')
        .factory('UserAppointmentsService', UserAppointmentsService);
    UserAppointmentsService.$inject = ['$http', '$httpParamSerializer'];
    /* @ngInject */
    function UserAppointmentsService($http, $httpParamSerializer) {
        var service = {
            query: query
        };
        return service;

        ////////////////

        function fetchData(response) {
            return response.data;
        }

        function query() {
            return $http.get('http://127.0.0.1:8000/user/api/get-appointments').then(fetchData);
        }
    }
})();