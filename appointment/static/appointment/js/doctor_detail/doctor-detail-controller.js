/**
 * Created by melika on 2/23/17.
 */
(function () {
    'use strict';
    angular
        .module('Base')
        .controller('DoctorController', DoctorController);
    DoctorController.$inject = ['DoctorDetailService', '$timeout', '$window', '$location'];
    /* @ngInject */
    function DoctorController(DoctorDetailService, $timeout, $window, $location) {
        var vm = this;
        vm.submit = submit;
        vm.showDialog = showDialog;

        activate();
        ////////////////

        function activate() {
            var splittedURL = $location.path().split('/');
            var id = splittedURL[splittedURL.length - 2];
            DoctorDetailService.getDoctor(id).then(function (data) {
                vm.doctor = data;
            });
            DoctorDetailService.getAppointments(id).then(function (data) {
                vm.dateAppointments = data;
                $timeout(function () {
                    angular.element("#persian-body").persiaNumber();
                }, 10)
            });
        }

        function submit() {
            DoctorDetailService.reserve($('#appointment').val())
                .then(function () {
                    Materialize.toast('نوبت شما با موفقیت رزرو گردید', 3000, 'rounded');
                    $timeout(function () {
                        $window.location.reload();
                    }, 1000);
                });
        }

        function showDialog(date, time, id) {
            var authenticated = localStorage.getItem('token')
            if (authenticated) {
                angular.element('#date').text(date);
                angular.element('#hour').text(time);
                angular.element('#appointment').val(id);
                angular.element('#confirm-dialog').modal('open');
            }
            else {
                angular.element('#login-modal').modal('open');
            }
        }
    }
})()