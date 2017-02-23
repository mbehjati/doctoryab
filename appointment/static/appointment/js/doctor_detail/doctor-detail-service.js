/**
 * Created by melika on 2/23/17.
 */

(function () {
    'use strict';
    angular
        .module('Base')
        .factory('DoctorDetailService', DoctorDetailService);
    DoctorDetailService.$inject = ['$http', '$httpParamSerializer'];
    /* @ngInject */
    function DoctorDetailService($http, $httpParamSerializer) {
        var service = {
            getAppointments: getAppointments,
            getDoctor: getDoctor,
            reserve: reserve
        };
        return service;

        ////////////////

        function getAppointments(id) {
            return $http.get('http://127.0.0.1:8000/appointment/doctor_times/' + id + '/').then(fetchData);
        }

        function getDoctor(id) {
            return $http.get('http://127.0.0.1:8000/appointment/get-doctor/' + id + '/').then(fetchData);

        }

        function reserve(appointmentId) {
            return $http.post('http://127.0.0.1:8000/appointment/api/reserve/', $httpParamSerializer({'appointment': appointmentId}), {headers: {'Content-Type': 'application/x-www-form-urlencoded'}});

        }

        function fetchData(response) {
            return response.data;
        }

    }
})()