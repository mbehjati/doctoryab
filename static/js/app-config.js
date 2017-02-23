/**
 * Created by melika on 2/22/17.
 */
(function () {
    angular.module('Base')
        .config(['$httpProvider', '$locationProvider', function ($httpProvider, $locationProvider) {
            $httpProvider.defaults.xsrfCookieName = 'csrftoken';
            $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
            $locationProvider.html5Mode(true);

        }]);
})();