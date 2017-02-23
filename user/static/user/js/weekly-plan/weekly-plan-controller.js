/**
 * Created by melika on 2/23/17.
 */
(function () {
    'use strict';
    angular
        .module('Base')
        .controller('WeeklyPlanController', WeeklyPlanController);
    WeeklyPlanController.$inject = ['WeeklyPlanService', '$timeout'];

    /* @ngInject */
    function WeeklyPlanController(WeeklyPlanService, $timeout) {
        var vm = this;
        vm.submit = submit;
        activate();

        ////////////////

        function activate() {
            WeeklyPlanService.query().then(function (data) {
                createSchedule(data);
            });
        }

        var datePicker = angular.element('.date-picker');

        datePicker.pDatepicker({
            observer: true,
            justSelectOnDate: true,
            autoClose: true,
            format: "YYYY-MM-DD",
            onSelect: function () {
                submit();
            }
        })
        ;
        function createSchedule(data) {
            vm.schedule = data;
            createTimeTable();
            $timeout(function () {
                angular.element("#persian-body").persiaNumber();
            }, 10)
        }

        function submit() {
            WeeklyPlanService.post({'date': vm.date}).then(function (data) {
                createSchedule(data)
            });
            datePicker.close();
        }

        function createTimeSlots() {
            var times = [];
            var min = ['00', '15', '30', '45'];
            var i;
            for (i = 0; i < 24; i++) {
                var str;
                if (i == 0)
                    str = '12:';
                else if (i > 12)
                    str = (i - 12) + ':';
                else
                    str = i + ':';
                for (var j = 0; j < 4; j++) {
                    var time_str;
                    time_str = str + min[j];
                    if (i >= 12)
                        time_str += 'pm';
                    else
                        time_str += 'am';
                    times.push(time_str);
                }

            }
            return times;
        }


        function createTimeTable() {
            var timeSlots = createTimeSlots();
            var min = timeSlots.length;
            var max = 0;
            var table = new Array(timeSlots.length);
            for (i = 0; i < timeSlots.length; i++) {
                table[i] = new Array(8).fill(0);
            }
            for (var i = 0; i < timeSlots.length; i++) {
                table[i][0] = timeSlots[i];
                for (var j = 1; j < 8; j++) {
                    angular.forEach(vm.schedule[j - 1].appointments, function (appointment) {
                        var startTime = appointment.start_time;
                        var patient = appointment.patient;
                        if (startTime == timeSlots[i]) {
                            if (i < min) min = i;
                            var value = (patient == null) ? 1 : 2;
                            var duration = appointment.duration / 15;
                            for (var d = 0; d < duration; d++) {
                                table[i + d][j] = value
                            }
                            if (i > max) max = i + duration;
                        }
                    });
                }
            }
            vm.table = table;
            vm.min = min;
            vm.max = max;
        }

    }
})
()