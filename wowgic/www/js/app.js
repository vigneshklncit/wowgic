// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.controllers' is found in controllers.js
angular.module('starter', ['ionic', 'starter.controllers', 'ionicLazyLoad'])



.run(function($ionicPlatform, $rootScope, $ionicHistory) {


  document.addEventListener("online", function online(){
      $rootScope.appError = false;
  }, false);
  document.addEventListener("offline", function offline(){
    $rootScope.appError = true;
    
  }, false);

/*
  $rootScope.$on('$stateChangeStart', function (event, toState, toStateParams, fromState, fromStateParams) {

    console.log("Changing state to :");
    console.log(toState);
      if(toState.name === 'facebook' ) {

     //   ionic.Platform.exitApp();
        
      }

  });
    $rootScope.$ionicGoBack = function(backCount) {
      alert(1);
      $ionicHistory.goBack(-2);
    };*/

  $ionicPlatform.ready(function() {
    $ionicPlatform.registerBackButtonAction(function (event) {
   // alert($ionicHistory.backView().stateName);
  if ($ionicHistory.backView().stateName === 'facebook' || $ionicHistory.currentStateName()==='facebook'){
    ionic.Platform.exitApp(); // stops the app
  } else {
    $ionicHistory.goBack();
  }
}, 100);

    // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
    // for form inputs)
    if (window.cordova && window.cordova.plugins.Keyboard) {
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      cordova.plugins.Keyboard.disableScroll(true);

    }
    if (window.StatusBar) {
      // org.apache.cordova.statusbar required
      StatusBar.styleDefault();
    }
  });
})
 .factory('timeoutHttpIntercept', function ($rootScope, $q) {
    return {
      'request': function(config) {
        config.timeout = 10000;
        return config;
      }
    };
 })
.config(function($stateProvider, $urlRouterProvider, $httpProvider) {

  $httpProvider.interceptors.push('timeoutHttpIntercept');

  $stateProvider


  .state('carousel',{
    url: '/carousel',
    templateUrl: 'templates/carousel.html'
  })

  .state('facebook',{
    url: '/facebook',
    templateUrl: 'templates/facebook.html',
    controller: 'fbCtrl'
  })

  .state('instagram',{
    url: '/instagram',
    templateUrl: 'templates/instagram.html'
  })

  .state('twitter',{
    url: '/twitter',
    templateUrl: 'templates/twitter.html'
  })

  .state('app', {
    url: '/app',
    abstract: true,
    templateUrl: 'templates/menu.html',
    controller: 'AppCtrl'
  })

  .state('app.search', {
    url: '/search',
    views: {
      'menuContent': {
        templateUrl: 'templates/search.html'
      }
    }
  })
  .state('app.feeds', {
      url: '/feeds?mongoid&count',
      views: {
        'menuContent': {
          templateUrl: 'templates/feeds.html',
          controller: 'feedsCtrl'
        }
      }
  }
  )

  .state('app.settings', {
      url: '/settings',
      views: {
        'menuContent': {
          templateUrl: 'templates/settings.html',
          controller: 'settingsCtrl'
        }
      }
  })
  .state('app.single', {
    url: '/profile/:profileid',
    views: {
      'menuContent': {
        templateUrl: 'templates/profile.html',
        controller: 'profileCtrl'
      }
    }
  });
  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/facebook');
});
