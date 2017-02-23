/**
 * Created by melika on 2/22/17.
 */
(function () {
    'use strict';
    angular
        .module('Base')
        .controller('BaseController', baseController);
    baseController.$inject = ['AccountsService', '$timeout', '$window'];
    /* @ngInject */
    function baseController(AccountsService, $timeout, $window) {
        var vm = this;
        vm.submitLogin = submitLogin;
        vm.message = ''

        activate();
        ////////////////

        function activate() {
            angular.element('.modal').modal();
        }

        function formData() {
            return {
                'username': vm.username,
                'password': vm.password
            };
        }

        function submitLogin() {
            console.log('dfaf', formData());
            AccountsService.login(formData())
                .then(success)
                .catch(incorrectInput);
        }

        function incorrectInput() {
            vm.message = 'نام کاربری یا گذرواژه شما اشتباه است'
        }

        function success(token) {
            AccountsService.saveAccount(token);
            AccountsService.realLogin(formData());
            showMessage();
        }

        function showMessage() {
            Materialize.toast('کاربر عزیز خوش آمدید.', 3000, 'rounded');
            angular.element('#login-modal').modal('close');
            $timeout(function () {
                $window.location.reload();
            }, 1000);
        }

    }
})();