/**
 * Created by melika on 2/23/17.
 */

(function () {
    'use strict';
    angular
        .module('Base')
        .controller('UserAppointmentsController', UserAppointmentsController);
    UserAppointmentsController.$inject = ['UserAppointmentsService', '$timeout', '$window'];
    /* @ngInject */
    function UserAppointmentsController(UserAppointmentsService, $timeout, $window) {
        var vm = this;

        activate();

        ////////////////
        function activate() {
            UserAppointmentsService.query().then(function (data) {
                vm.appointments = data;
                $timeout(function () {
                    angular.element("#persian-body").persiaNumber();
                }, 10)
            })
        }

    }
})();