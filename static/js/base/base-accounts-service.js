/**
 * Created by melika on 2/22/17.
 */
(function () {
    'use strict';
    angular
        .module('Base')
        .factory('AccountsService', AccountsService);
    AccountsService.$inject = ['$http', '$httpParamSerializer', '$window'];
    /* @ngInject */
    function AccountsService($http, $httpParamSerializer, $window) {
        var service = {
            login: login,
            logout: logout,
            saveAccount: saveToken,
            realLogin: realLogin
        };
        return service;
        ////////////////

        function login(data) {
            return $.post('http://127.0.0.1:8000/get_auth_token/', data);
            // return $http.post('http://127.0.0.1:8000/get_auth_token/', data);
        }

        function logout() {
            $window.localStorage.setItem('token', '');
        }

        function saveToken(response) {
            var token = response.token;
            $window.localStorage.setItem('token', token);
        }

        function realLogin(data) {
            $http.post('http://127.0.0.1:8000/user/login/', $httpParamSerializer(data), {headers: {'Content-Type': 'application/x-www-form-urlencoded'}});
        }
    }
})();