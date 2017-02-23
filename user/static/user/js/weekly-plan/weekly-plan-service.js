/**
 * Created by melika on 2/23/17.
 */
(function () {
    'use strict';
    angular
        .module('Base')
        .factory('WeeklyPlanService', WeeklyPlanService)

    WeeklyPlanService.$inject = ['$http', '$httpParamSerializer'];
    /* @ngInject */
    function WeeklyPlanService($http, $httpParamSerializer) {
        var service = {
            query: query,
            post: post
        };
        return service;
        ////////////////

        function fetchData(response) {
            return response.data;
        }

        function query() {
            return $http.get('http://127.0.0.1:8000/user/api/doctor-weekly-plan').then(fetchData);
        }

        function post(data) {
            return $http.post('http://127.0.0.1:8000/user/api/doctor-weekly-plan', $httpParamSerializer(data), {headers: {'Content-Type': 'application/x-www-form-urlencoded'}}).then(fetchData);
        }
    }

})();