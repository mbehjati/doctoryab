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
            return $http.get('https://doctoryab.herokuapp.com/appointment/doctor_times/' + id + '/').then(fetchData);
        }

        function getDoctor(id) {
            return $http.get('https://doctoryab.herokuapp.com/appointment/get-doctor/' + id + '/').then(fetchData);

        }

        function reserve(appointmentId) {
            return $http.post('https://doctoryab.herokuapp.com/appointment/api/reserve/', $httpParamSerializer({'appointment': appointmentId}), {headers: {'Content-Type': 'application/x-www-form-urlencoded'}});

        }

        function fetchData(response) {
            return response.data;
        }

    }
})()