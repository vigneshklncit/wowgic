  angular.module('starter.controllers', ['ngCordova', 'angularMoment'])

  /*Filter starts here*/
  .filter('getById', function() {
    return function(input, id) {
      console.log('input ',input);

      var i=0, len= input.length;
      for (; i<len; i++) {
        if (input[i].id == id) {
          return input[i];
        }
      }
      return null;
    }
  })

  /* may be re-used
  .filter('datetime', function($filter) {
    return function(input) {
      if(input == null){ 
        return ""; 
      } 
    var _date = $filter('date')(new Date(input),'MMM dd yyyy - HH:mm:ss');
    return _date.toUpperCase();
   };

  })*/
  /*Filter Ends here*/

  /*Factory starts here*/
  .factory('dataFactory', ['$http','$window', '$rootScope', function($http, $window, $rootScope) {

      var browser = false;
      var app = document.URL.indexOf( 'http://' ) === -1 && document.URL.indexOf( 'https://' ) === -1;
      if (app) {
        browser = false;
      // PhoneGap application
      } else {
        browser = true;
      // Web page
      }
      //var urlBase = 'http://wowgicflaskapp-wowgic.rhcloud.com';
      var urlBase = 'http://104.251.215.131:8080';
      var dataFactory = {};
      var code = '0a1932b22820439b95511e581c4fd8e4';

      dataFactory.wowgicLogin = function (data) {
        if(browser) {
          return $http.get(urlBase+'/FBTesting',data);
        }
        else {
        //return $http.get(urlBase+'/FBTesting',data);  
         return $http.post(urlBase+'/FBLogin',data);
        }
      };
      
      /*2nd time user*/
      dataFactory.fetchAllfeeds = function (mongoid,count) {

        var id = localStorage.getItem('userid');
        if(mongoid){
          if(count){
            count = '&count=' + count;  
          }
          else{
            count='';
          }
          
          return $http.get(urlBase+'/displayFeeds?collId='+mongoid+count);
        }
        else{
          return $http.get(urlBase+'/refreshUserFeeds');
        }
                
      };

      dataFactory.renewoath = function () {
          return $http.post(urlBase+'/renewAuth',{password:localStorage.getItem('wowgicpassword')}); 
      };

      dataFactory.getNearby = function (lat,lng, radius) {
        data= {     
              "lat": lat,
              "lng": lng,
              "distance":radius
        }
        return $http.post(urlBase+'/locationFeeds',data); 
      };
      return dataFactory; 

  }])
  /*Factory Ends here*/

  /*Service starts here*/
  .service('fbService', ['$cordovaFacebook', function() {
  //  var response = {"id": 435354545454, "name":"chellad"};
    var response = null;
    var setData = function(userdata) {
      response = userdata;
    };

    var getData = function() {
      return response;
    }

    return {
      setData: setData,
      getData: getData
    };

  }])

  /*Service Ends here*/


  /*Facebook login starts here*/
  .controller('fbCtrl', function($scope, $cordovaFacebook, $state, fbService, $timeout, $window, $http, $cordovaAppAvailability) {

      if(localStorage.getItem("userid") && localStorage.getItem("userid")!='null'){
      //  $state.go("app.feeds");
        $state.go('app.feeds', {}, {location:'replace'});
      }

      $scope.fbsignin = function() {

          $cordovaFacebook.login(["public_profile", "email", "user_friends","user_photos","user_status","user_education_history","user_hometown","user_location","user_tagged_places","user_work_history","user_likes"])
              .then(function(userdetails) {
                 $scope.fbuserdetails();
              
              }, 
              function(error) {     
                console.log('errorfb', error);
                $cordovaFacebook.login(["public_profile", "email", "user_friends","user_photos","user_status","user_education_history","user_hometown","user_location","user_tagged_places","user_work_history","user_likes"])
                .then(function(userdetails) {
                  $scope.fbuserdetails();
                });
              });
      }

      $scope.fbuserdetails = function() {
        $cordovaFacebook.api("/me?fields=id,name,hometown,location,education,work", ["user_friends"])
          .then(function(userdata) {
            localStorage.setItem("userid", userdata.id);          
            fbService.setData(userdata);
           // $state.go("app.feeds");
           $state.go('app.feeds', {}, {location:'replace'});
          }, function(error) {
              console.log(error);
              $scope.fbsignin();
          //    $state.go("facebook");
          });
      }
  })
  /*Facebook controller ends here*/

  .controller('AppCtrl', function($scope, $ionicModal, $timeout, dataFactory, fbService, $filter, $state, $ionicLoading, $http, $ionicHistory, $rootScope) {

    // With the new view caching in Ionic, Controllers are only called
    // when they are recreated or on app start, instead of every page change.
    // To listen for when this page is active (for example, to refresh data),
    // listen for the $ionicView.enter event:
    //$scope.$on('$ionicView.enter', function(e) {
    //});

    // Form data for the login modal
    $scope.feeds = [];
    $scope.errorjs = false;
    var feeds;
    renewoath = function(callback,params) {
      $ionicLoading.show({
          template: 'Validating authenticaition'
      }); 
      dataFactory.renewoath().success(function(resp) {
        localStorage.setItem('wowgictoken',resp.Authorization);
        $http.defaults.headers.common.Authorization = resp.Authorization;
        if(!params) {
          callback();  
        }
        else {
          callback(params);  
        }
      }).error(function(error,status,thrown){
        feedErrors(error,status,thrown);
      });
    }


  function feedErrors(error,status,thrown) {
    $ionicLoading.hide();
        alert('error'+error);
        switch(status) {
          case 503:
            $scope.errorjs = "we're under maintanance. try after sometime";
          break;
          case 500:
            $scope.errorjs = "Something went wrong. try later";
          break;
          case 401:
            $scope.errorjs = "Sorry!! your not authorized to view this page";
          break;
          case 403:
            renewoath($scope.fetchAllfeeds);
          break;
          default:
            $scope.errorjs = "Some error has occured. Please try after sometime";

        }
  }

    $scope.loginWowgic = function () {
      var s=fbService.getData();
      console.log('check111'+s);
      console.log('in loginWowgic');
      //console.log(Object.keys(s));
    //  console.log(s.id);
      console.log('in loginWowgic1');
      dataFactory.wowgicLogin(fbService.getData()).success(function(resp) {
      feeds = resp;
      localStorage.setItem('wowgicpassword',resp.password);
      localStorage.setItem('wowgictoken',resp.Authorization);
      
      $http.defaults.headers.common.Authorization = resp.Authorization;
      $scope.fetchAllfeeds();
      }).error(function(error,status,thrown) {
        feedErrors(error,status,thrown);
      });
    }

    $scope.fetchAllfeeds = function (mongoid,count) {
      $scope.errorjs=false;
      $scope.feeds=[];
     // $state.go("app.feeds");
      $ionicLoading.show({
        template: 'Wowing...'
       });

      dataFactory.fetchAllfeeds(mongoid,count).success(function(resp) {
      feeds = resp;
      var data=[];
      angular.forEach(resp, function(key, value) {
          
          if(key.created_at) {
            data.push(parseTwitter(key));
            console.log('twitter');
          }
          else {
            data.push(parseInstagram(key));
            console.log('instagram');
          }
        
        });
      $scope.feeds = data;
      for(var i=0;i<data.length;i++){
        console.log(data[i].source+' ** ' +data[i].time);    
      }
      console.log('over');
      $ionicLoading.hide();
      
      if(!feeds.length) {
        $scope.errorjs = 'No feeds this time :( try later';
      }

      }).error(function(error,status,thrown) {
        feedErrors(error,status,thrown);
      });
    }

    $scope.data = {
      radius:5
    };
    $scope.getNearby = function () {
      $scope.errorjs=false;
      $scope.feeds=[];
      $ionicLoading.show({template: 'fetching Location'}); 
      $state.go("app.feeds");
      if (navigator.geolocation) {
        var options = {maximumAge: 0, timeout: 10000, enableHighAccuracy:true};
        navigator.geolocation.getCurrentPosition($scope.showPosition, $scope.showError, options);
      }
      else {
        alert('not available');
        $ionicLoading.hide();
        $scope.error = "Geolocation is not supported in your device.";
      }
    }
    $scope.showPosition = function (position) {
      var lat = position.coords.latitude;
      var lng = position.coords.longitude;
      var data=[];
      $ionicLoading.show({template: 'fetching nearby news'}); 
      $scope.$apply();
      dataFactory.getNearby(lat,lng,$scope.data.radius).success(function(resp) { 
      feeds = resp;
      $scope.feeds=[];

      angular.forEach(resp, function(key, value) {
          
          if(key.created_at) {
            data.push(parseTwitter(key));
            console.log('twitter');
          }
          else {
            data.push(parseInstagram(key));
            console.log('instagram');
          }
        
        });
      $scope.feeds = data;
      /*
      angular.forEach(resp, function(key, value) {

          if(key.created_at) {

            parseTwitter(key)
            console.log(key.created_at);
          }
          else {
            parseInstagram(key)
          }
      });*/
      $ionicLoading.hide();
      }).error(function(error){ 
        $ionicLoading.hide();
        alert('error'+error);
        status= (!!error)?error.status:null;
        switch(status) {
          case 503:
            $scope.errorjs = "we're under maintanance. try after sometime";
          break;
          case 500:
            $scope.errorjs = "Something went wrong. try later";
          break;
          case 401:
            $scope.errorjs = "Sorry!! your not authorized to view this page";
          break;
          case 403:
            renewoath($scope.showPosition, position);
          break;
          default:
            $scope.errorjs = "Some error has occured. Please try after sometime";

        }

      });
    }

    $scope.showError = function (error) {
      $scope.feeds=[];
      switch (error.code) {
        case error.PERMISSION_DENIED:
          $scope.errorjs = "User denied the request for Geolocation."
        break;
        case error.POSITION_UNAVAILABLE:
          $scope.errorjs = "Location information is unavailable."
        break;
        case error.TIMEOUT:
          $scope.errorjs = "The request to get user location timed out."
        break;
        case error.UNKNOWN_ERROR:
          $scope.errorjs = "An unknown error occurred."
        break;
        default:
          $scope.errorjs = "Unable to find your location. Please switch on location"
      }
      $ionicLoading.hide();
      console.log($scope.errorjs);
      $scope.$apply();
    }
    $scope.gotoSettings = function(){
       $state.go('app.settings');
    }

    $scope.openOtherApps = function () {

    var scheme,scheme_prefix, url;
 
    // Don't forget to add the org.apache.cordova.device plugin! 
    if(device.platform === 'iOS') {
      if($scope.source === 'twitter') {
        scheme = 'twitter://';
        scheme_prefix = scheme;
      }
      else {
        scheme = 'instagram://';  
        cheme_prefix = scheme;     
      }
    }
    else if(device.platform === 'Android') {
      if($scope.source === 'twitter') {
        scheme = 'com.twitter.android';
        scheme_prefix = 'twitter://';
        url = scheme_prefix + 'user?screen_name=' + $scope.username;
      }
      else {
        scheme  = 'com.instagram.android';
        scheme_prefix = 'instagram://';
        var url = scheme_prefix + 'user?username=' + $scope.username;
      }
        
    }
     
    appAvailability.check(
        scheme,  
             // URI Scheme or Package Name 
        function() {  // Success callback 
            window.open(url, '_system', 'location=no');
        },
        function() {  // Error callback 
            alert(scheme + ' is not available :(');
        }
      );
    }

    $scope.gotoprofile = function(id) {
        var singlefeed = $filter('getById')(feeds, id);
        console.log('singlefeed',singlefeed);
        if(singlefeed.created_time) {
          //INSTAGRAM
          $scope.profile_image = singlefeed.user.profile_picture;
          $scope.showdetails = false;
          $scope.name = singlefeed.user.full_name;
          $scope.username = singlefeed.user.username;
          $scope.source = "instagram";


        }
        else {
        //TWITTER
        $scope.profile_image = singlefeed.user.profile_image_url;
        $scope.followers = singlefeed.user.followers_count;
        $scope.following = singlefeed.user.friends_count;
        $scope.description = singlefeed.user.description;
        $scope.name = singlefeed.user.name;
        $scope.username = singlefeed.user.screen_name;
        $scope.source = "twitter";
        $scope.showdetails = true;
      }
      $state.go('app.single');
       
    }

      var parseTwitter = function(obj) {
      var fata= {};
      fata.id = obj.id;
      fata.time =  new Date(obj.created_at);
      fata.text = obj.text;
      fata.user= {};
      fata.user.name = obj.user.screen_name;
      fata.image =  obj.entities.media ? obj.entities.media[0].media_url : null;
      fata.user.profile_image = obj.user.profile_image_url;
      fata.location = obj.place? obj.place.name : null;
      fata.source='twitter';
      return fata;
      //$scope.feeds.push(fata);
    //  console.log($scope.feeds);
    }

      var parseInstagram= function(obj) {
      var fata= {};
        if(obj.id) {
          fata.id = obj.id;
          fata.time =  new Date(parseInt(obj.created_time) * 1000);
         // fata.time = obj.created_time;
          fata.text = obj.caption ? obj.caption.text : null;
          fata.user= {};
          fata.image = obj.images.standard_resolution.url;
          fata.user.name = obj.user.username;
          fata.user.profile_image = obj.user.profile_picture;
          fata.location = obj.location ? obj.location.name : null;
          fata.source='Instagram';
          return fata;
          //$scope.feeds.push(fata);
          console.log(obj.created_time);
          console.log(fata.text);
      }
    }
    //init();
  })


  .controller('settingsCtrl', function($scope,$state, $ionicHistory) {
    $scope.logout = function() {
      localStorage.setItem('userid',null);
      localStorage.setItem('wowgicpassword',null);
      localStorage.setItem('wowgictoken',null);
      $ionicHistory.clearHistory();
      $ionicHistory.clearCache();
      $scope.feeds= [];
      $state.go('facebook');
      //location.reload();
    }
  })



  .controller('feedsCtrl', function($scope, $stateParams, $rootScope,dataFactory, fbService, $ionicLoading, $http) {
  function init(){
    $ionicLoading.show({
        template: 'Wowing...'
    }); 
    var data = fbService.getData();

    if(data) {
      //first time user
      $scope.loginWowgic();  
    }
    else {
      if(localStorage.getItem('wowgictoken') && localStorage.getItem('wowgictoken')!='null'){
        $http.defaults.headers.common.Authorization = localStorage.getItem('wowgictoken');
        $scope.fetchAllfeeds($stateParams.mongoid,$stateParams.count);
      }
      else{
        $scope.loginWowgic();
      }
    }
  }

  init();
  })

  .controller('profileCtrl', function($scope, $state, $stateParams) {

    $scope.profiletitle =  $stateParams.profileid;
  });


  moment.locale('en', {
      relativeTime : {
          future: "in %s",
          past:   "%s",
          s:  "sec",
          m:  "1m",
          mm: "%dm",
          h:  "1h",
          hh: "%dh",
          d:  "1d",
          dd: "%dd",
          M:  "1month",
          MM: "%dmonths",
          y:  "1yr",
          yy: "%dyrs"
      }
  })

  /*

    $scope.loginData = {};

    // Create the login modal that we will use later
    $ionicModal.fromTemplateUrl('templates/login.html', {
      scope: $scope
    }).then(function(modal) {
      $scope.modal = modal;
    });

    // Triggered in the login modal to close it
    $scope.closeLogin = function() {
      $scope.modal.hide();
    };

    // Open the login modal
    $scope.login = function() {
      $scope.modal.show();
    };

    // Perform the login action when the user submits the login form
    $scope.doLogin = function() {
      console.log('Doing login', $scope.loginData);

      // Simulate a login delay. Remove this and replace with your login
      // code if using a login system
      $timeout(function() {
        $scope.closeLogin();
      }, 1000);
    };
  */
